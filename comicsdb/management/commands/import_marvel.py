import dateutil.relativedelta
import marvelous
from comicsdb.models import Character, Creator, Credits, Issue, Role, Series
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.text import slugify
from metron.settings import MARVEL_PRIVATE_KEY, MARVEL_PUBLIC_KEY
from simple_history.utils import update_change_reason

from ._parse_title import FileNameParser
from ._utils import select_list_choice


class Command(BaseCommand):
    help = "Retrieve next months comics from the Marvel API."

    def _fix_role(self, role):
        if role == "penciler":
            return "penciller"
        elif "cover" in role:
            return "cover"
        else:
            return role

    def _add_characters(self, marvel_data, issue_obj):
        for character in marvel_data.characters:
            try:
                c = Character.objects.get(name__iexact=character.name)
                issue_obj.characters.add(c)
            except Character.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Unable to find '{character.name}'. Skipping...\n"
                    )
                )
                continue

    def _add_creators(self, marvel_data, issue_obj):
        for creator in marvel_data.creators:
            try:
                self.stdout.write(f"Searching database for {creator.name}...")
                results = Creator.objects.filter(name__unaccent__icontains=creator.name)
                if not results:
                    first, *_, last_name = creator.name.split()
                    results = Creator.objects.filter(
                        name__unaccent__icontains=last_name
                    )
                    # If results are more than 15 let's try narrowing the results.
                    if len(results) > 15:
                        new_results = results.filter(name__unaccent__icontains=first)
                        if new_results:
                            results = new_results

                if results:
                    correct_creator = select_list_choice(results)
                    r = self._fix_role(creator.role)
                    role = Role.objects.get(name__iexact=r)
                    credits = Credits.objects.create(
                        issue=issue_obj, creator=correct_creator
                    )
                    credits.role.add(role)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Added {correct_creator} as a {role} to {issue_obj}\n"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Unable to find {creator.name}. Skipping...\n"
                        )
                    )
            except Creator.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"Unable to find {creator.name}. Skipping...\n")
                )
                continue

    def _add_eic_credit(self, issue_obj):
        cb = Creator.objects.get(slug="c-b-cebulski")
        cr, create = Credits.objects.get_or_create(issue=issue_obj, creator=cb)
        self.stdout.write(self.style.SUCCESS(f"Added credit for {cb} to {issue_obj}."))
        if create:
            eic = Role.objects.get(name__iexact="editor in chief")
            cr.role.add(eic)
            self.stdout.write(
                self.style.SUCCESS(f"Added '{eic}' role for {cb} to {issue_obj}.\n")
            )

    def _determine_cover_date(self, release_date):
        new_date = release_date + dateutil.relativedelta.relativedelta(months=2)
        return new_date.replace(day=1)

    def add_issue_to_database(self, series_obj, fnp: FileNameParser, marvel_data):
        cover_date = self._determine_cover_date(marvel_data.dates.on_sale)
        slug = slugify(series_obj.slug + " " + fnp.issue)

        try:
            issue, create = Issue.objects.get_or_create(
                series=series_obj,
                number=fnp.issue,
                slug=slug,
                store_date=marvel_data.dates.on_sale,
                cover_date=cover_date,
            )
            if marvel_data.description:
                issue.desc = marvel_data.description
                issue.save()

            if create:
                self._add_eic_credit(issue)
                if marvel_data.creators:
                    self._add_creators(marvel_data, issue)
                if marvel_data.characters:
                    self._add_characters(marvel_data, issue)
                # Save the change reason
                update_change_reason(issue, "Marvel import")
                self.stdout.write(self.style.SUCCESS(f"Added {issue} to database.\n\n"))
            else:
                self.stdout.write(self.style.WARNING(f"{issue} already exists...\n\n"))
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(
                    f"{series_obj} #{fnp.issue} already existing in the database.\n\n"
                )
            )

    def _get_data_from_marvel(self, options):
        m = marvelous.api(MARVEL_PUBLIC_KEY, MARVEL_PRIVATE_KEY)
        return sorted(
            m.comics(
                {
                    "format": "comic",
                    "formatType": "comic",
                    "noVariants": True,
                    "dateDescriptor": options["date"],
                    "limit": 100,
                }
            ),
            key=lambda comic: comic.title,
        )

    def add_arguments(self, parser):
        parser.add_argument(
            "-d",
            "--date",
            type=str,
            default="nextWeek",
            help="The date period to query.",
        )

    def handle(self, *args, **options):
        if not options["date"]:
            self.stdout.write(self.style.NOTICE("No month requested. Exiting..."))
            exit(0)

        pulls = self._get_data_from_marvel(options)

        fnp = FileNameParser()
        for comic in pulls:
            fnp.parse_filename(comic.title)
            self.stdout.write(f"Searching database for {fnp.series} #{fnp.issue}")
            results = Series.objects.filter(name__icontains=fnp.series)
            # If results are more than 15 let's try narrowing the results.
            if len(results) > 15:
                new_results = Series.objects.filter(
                    name__icontains=fnp.series, year_began=int(fnp.year)
                )
                if new_results:
                    results = new_results

            if results:
                correct_series = select_list_choice(results)
                if correct_series:
                    self.add_issue_to_database(correct_series, fnp, comic)
                else:
                    self.stdout.write(
                        self.style.NOTICE(
                            f"Not adding {fnp.series} #{fnp.issue} to database.\n\n"
                        )
                    )
            else:
                self.stdout.write(f"No series in database for {fnp.series}\n\n")
