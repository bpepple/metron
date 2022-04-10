import shutil
import tempfile
from datetime import datetime
from decimal import Decimal
from os import fspath
from pathlib import Path
from urllib.request import urlopen

import dateutil.relativedelta
import esak
from boto3 import session
from boto3.s3.transfer import S3Transfer
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.text import slugify

from comicsdb.models import Arc, Character, Creator, Credits, Issue, Role, Series
from comicsdb.models.attribution import Attribution
from metron.settings import DEBUG, MARVEL_PRIVATE_KEY, MARVEL_PUBLIC_KEY
from metron.storage_backends import MediaStorage

from ._parse_title import FileNameParser
from ._utils import select_list_choice

if not DEBUG:
    from metron.settings import (
        AWS_ACCESS_KEY_ID,
        AWS_S3_ENDPOINT_URL,
        AWS_SECRET_ACCESS_KEY,
        AWS_STORAGE_BUCKET_NAME,
    )
else:
    from metron.settings import MEDIA_ROOT


class Command(BaseCommand):
    help = "Retrieve next months comics from the Marvel API."

    @property
    def get_upload_image_path(self):
        now = datetime.now()
        return f"issue/{now:%Y/%m/%d}/"

    def _upload_image(self, image):
        # TODO: Should probably use Storage to upload image instead of boto directly
        media_storage = MediaStorage()
        upload_file = f"{media_storage.location}/{self.get_upload_image_path}{image.name}"

        sesh = session.Session()
        client = sesh.client(
            "s3",
            region_name="nyc3",
            endpoint_url=AWS_S3_ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        transfer = S3Transfer(client)
        transfer.upload_file(
            str(image),
            AWS_STORAGE_BUCKET_NAME,
            upload_file,
            extra_args={"CacheControl": "max-age=604800", "ACL": "public-read"},
        )
        self.stdout.write(self.style.SUCCESS(f"Uploaded {image.name} to DigitalOcean."))

    def _fix_role(self, role):
        if role == "penciler":
            return "penciller"
        elif "cover" in role:
            return "cover"
        else:
            return role

    def _check_for_solicit_txt(self, text_objects):
        return next((i.text for i in text_objects if i.type == "issue_solicit_text"), None)

    def _add_characters(self, characters, issue_obj):
        for character in characters:
            try:
                self.stdout.write(f"Searching database for {character.name}...")
                results = Character.objects.filter(name__unaccent__icontains=character.name)
                if not results:
                    words = character.name.split()
                    results = Character.objects.filter(name__unaccent__icontains=words[0])
                    # If results are more than 15 let's try narrowing the results.
                    if results.count() > 15:
                        if new_results := results.filter(name__unaccent__icontains=words[-1]):
                            results = new_results

                if results:
                    if correct_character := select_list_choice(results):
                        issue_obj.characters.add(correct_character)
                        self.stdout.write(
                            self.style.SUCCESS(f"Added {character.name} to {issue_obj}\n")
                        )
            except Character.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"Unable to find '{character.name}'. Skipping...\n")
                )
                continue

    def _add_arcs(self, events, issue_obj):
        for e in events:
            try:
                self.stdout.write(f"Searching database for {e.name}...")
                if results := Arc.objects.filter(name__icontains=e.name):
                    correct_arc = select_list_choice(results)
                    if correct_arc and correct_arc not in issue_obj.arcs.all():
                        issue_obj.arcs.add(correct_arc)
                        self.stdout.write(
                            self.style.SUCCESS(f"Added {e.name} to {issue_obj}\n")
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"{e.name} already added to {issue_obj}. Skipping...\n"
                            )
                        )

                else:
                    self.stdout.write(
                        self.style.WARNING(f"Unable to find {e.name}. Skipping...\n")
                    )
            except Creator.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"Unable to find {e.name}. Skipping...\n")
                )
                continue

    def _add_creators(self, creators, issue_obj):
        for creator in creators:
            try:
                self.stdout.write(f"Searching database for {creator.name}...")
                results = Creator.objects.filter(name__unaccent__icontains=creator.name)
                if not results:
                    first, *_, last_name = creator.name.split()
                    results = Creator.objects.filter(name__unaccent__icontains=last_name)
                    # If results are more than 15 let's try narrowing the results.
                    if results.count() > 15:
                        if new_results := results.filter(name__unaccent__icontains=first):
                            results = new_results

                if results and (correct_creator := select_list_choice(results)):
                    r = self._fix_role(creator.role)
                    role = Role.objects.get(name__iexact=r)
                    credits = Credits.objects.create(issue=issue_obj, creator=correct_creator)
                    credits.role.add(role)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Added {correct_creator} as a {role} to {issue_obj}\n"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Unable to find {creator.name}. Skipping...\n")
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

    def _download_image(self, url):
        url_path = Path(url)
        save_path = Path(tempfile.gettempdir()) / url_path.name
        with open(save_path, "wb") as img_file:
            img_file.write(urlopen(url).read())
        return save_path

    def _determine_cover_date(self, release_date):
        new_date = release_date + dateutil.relativedelta.relativedelta(months=2)
        return new_date.replace(day=1)

    def add_issue_to_database(
        self, series_obj, fnp: FileNameParser, marvel_data, add_creator: bool, cover: bool
    ):
        # Marvel store date is in datetime format.
        store_date = marvel_data.dates.on_sale
        cover_date = self._determine_cover_date(store_date)
        slug = slugify(f"{series_obj.slug} {fnp.issue}")

        try:
            issue, create = Issue.objects.get_or_create(
                series=series_obj,
                number=fnp.issue,
                slug=slug,
                store_date=store_date,
                cover_date=cover_date,
            )

            modified = False

            if not issue.desc and marvel_data.text_objects:
                if solicit := self._check_for_solicit_txt(marvel_data.text_objects):
                    issue.desc = solicit
                    self.stdout.write(self.style.SUCCESS(f"Added description to {issue}."))
                    modified = True

            if not issue.price and marvel_data.prices.print > Decimal("0.00"):
                issue.price = marvel_data.prices.print
                self.stdout.write(
                    self.style.SUCCESS(f"Add price of '{marvel_data.prices.print}' to {issue}")
                )
                modified = True

            if not issue.upc and marvel_data.upc:
                issue.upc = marvel_data.upc
                self.stdout.write(
                    self.style.SUCCESS(f"Added UPC of '{marvel_data.upc}' to {issue}.")
                )
                modified = True

            if not issue.page and marvel_data.page_count:
                issue.page = marvel_data.page_count
                self.stdout.write(self.style.SUCCESS(f"Added page count to {issue}."))
                modified = True

            if marvel_data.events:
                self._add_arcs(marvel_data.events, issue)

            if modified:
                if marvel_data.urls.detail:
                    issue.attribution.create(
                        source=Attribution.Source.MARVEL, url=marvel_data.urls.detail
                    )
                issue.save()

            if create:
                if cover:
                    if DEBUG:
                        self._get_cover_debug(marvel_data, issue)

                    else:
                        self._get_cover(marvel_data, issue)
                self._add_eic_credit(issue)

                if add_creator and marvel_data.creators:
                    self._add_creators(marvel_data.creators, issue)

                if marvel_data.characters:
                    self._add_characters(marvel_data.characters, issue)

                self.stdout.write(self.style.SUCCESS(f"Added {issue} to database.\n\n"))
            elif cover and not issue.image:
                if not DEBUG:
                    self._get_cover(marvel_data, issue)
                else:
                    self._get_cover_debug(marvel_data, issue)
                self.stdout.write(self.style.SUCCESS(f"Added image to {issue}\n"))
            else:
                self.stdout.write(self.style.WARNING(f"{issue} already exists...\n\n"))
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(
                    f"{series_obj} #{fnp.issue} already existing in the database.\n\n"
                )
            )

    def _get_cover_debug(self, marvel_data, issue):
        fn = self._download_image(marvel_data.images[0])
        issue.image = f"{self.get_upload_image_path}{fn.name}"
        issue.save()

        dest = Path(MEDIA_ROOT) / f"{self.get_upload_image_path}"
        if not dest.is_dir():
            dest.mkdir(parents=True)
        shutil.move(fspath(fn), fspath(dest))

    def _get_cover(self, marvel_data, issue):
        fn = self._download_image(marvel_data.images[0])
        issue.image = f"{self.get_upload_image_path}{fn.name}"
        issue.save()
        self._upload_image(fn)
        fn.unlink()

    def _get_data_from_marvel(self, options):
        m = esak.api(MARVEL_PUBLIC_KEY, MARVEL_PRIVATE_KEY)
        if options["date"]:
            return sorted(
                m.comics_list(
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
        else:
            return sorted(
                m.comics_list(
                    {
                        "format": "comic",
                        "formatType": "comic",
                        "noVariants": True,
                        "dateRange": options["range"],
                    }
                ),
                key=lambda comic: comic.title,
            )

    def add_arguments(self, parser):
        parser.add_argument(
            "-d",
            "--date",
            type=str,
            help="The date period to query.",
        )
        parser.add_argument(
            "--range", type=str, help="Date range to query (e.g. 2013-01-01,2013-01-02)."
        )
        parser.add_argument(
            "-c", "--creators", action="store_true", help="Add creators to issue."
        )
        parser.add_argument(
            "--cover",
            help="Retrieve issue covers from Marvel.",
            action="store_true",
            default=False,
        )

    def handle(self, *args, **options):
        if not options["date"] and not options["range"]:
            self.stdout.write(self.style.NOTICE("No month requested. Exiting..."))
            exit(0)

        pulls = self._get_data_from_marvel(options)

        fnp = FileNameParser()
        for comic in pulls:
            fnp.parse_filename(comic.title)
            self.stdout.write(f"Searching database for {fnp.series} #{fnp.issue}")
            results = Series.objects.filter(name__icontains=fnp.series)
            # If results are more than 15 let's try narrowing the results.
            if results.count() > 15:
                if new_results := Series.objects.filter(
                    name__icontains=fnp.series, year_began=int(fnp.year)
                ):
                    results = new_results

            if results:
                if correct_series := select_list_choice(results):
                    self.add_issue_to_database(
                        correct_series, fnp, comic, options["creators"], options["cover"]
                    )
                else:
                    self.stdout.write(
                        self.style.NOTICE(
                            f"Not adding {fnp.series} #{fnp.issue} to database.\n\n"
                        )
                    )
            else:
                self.stdout.write(f"No series in database for {fnp.series}\n\n")
