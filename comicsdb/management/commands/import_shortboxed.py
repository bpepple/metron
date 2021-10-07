from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.text import slugify
from serifan import api
from serifan import exceptions as sb_err
from simple_history.utils import update_change_reason

from comicsdb.models import Issue, Series

from ._utils import (
    clean_description,
    clean_shortboxed_data,
    determine_cover_date,
    get_query_values,
    select_list_choice,
)


class Command(BaseCommand):
    help = "Retrieve weekly comics from Shortboxed.com"

    def __init__(self) -> None:
        super().__init__()
        self.talker = api()

    def add_issue_to_database(self, series_obj, issue_number, sb_data):
        cover_date = determine_cover_date(sb_data.release_date, sb_data.publisher)
        try:
            issue, create = Issue.objects.get_or_create(
                series=series_obj,
                number=issue_number,
                slug=slugify(series_obj.slug + " " + issue_number),
                store_date=sb_data.release_date,
                cover_date=cover_date,
            )

            modified = False
            if not issue.sku and sb_data.diamond_id:
                issue.sku = sb_data.diamond_id
                self.stdout.write(
                    self.style.SUCCESS(f"Added sku of '{sb_data.diamond_id}' to {issue}.")
                )
                modified = True

            if not issue.desc and sb_data.description:
                clean_desc = clean_description(sb_data.description)
                issue.desc = clean_desc.strip()
                self.stdout.write(self.style.SUCCESS(f"Added description to {issue}."))
                modified = True

            if not issue.price and sb_data.price:
                issue.price = sb_data.price
                self.stdout.write(
                    self.style.SUCCESS(f"Added price of ${issue.price} to {issue}.")
                )
                modified = True

            if modified:
                issue.save()

            if create:
                update_change_reason(issue, "Shortboxed import")
                self.stdout.write(self.style.SUCCESS(f"Added {issue} to database.\n\n"))
            else:
                self.stdout.write(self.style.WARNING(f"{issue} already exists...\n\n"))
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(
                    f"Integrity Error: {series_obj} #{issue_number} already existing in the database.\n\n"
                )
            )

    def add_arguments(self, parser):
        parser.add_argument(
            "-w", "--weeks", action="store_true", help="Show available release dates"
        )
        parser.add_argument(
            "-q", "--query", action="store_true", help="Query Shortboxed for release"
        )
        parser.add_argument("-p", "--publisher", type=str, help="The publisher to query")
        parser.add_argument(
            "-d", "--date", type=str, help="Enter a release date in YYYY-MM-DD format"
        )

    def handle(self, *args, **options):
        if not options["weeks"] and not options["query"]:
            self.stdout.write(self.style.NOTICE("No action requested. Exiting..."))
            exit(0)

        if options["weeks"]:
            NUMBER_OF_WEEKS = 5
            results = self.talker.available_release_dates()
            self.stdout.write(f"Last {NUMBER_OF_WEEKS} release dates:")
            for i in results[-NUMBER_OF_WEEKS:]:
                self.stdout.write(f"{i}")

        if options["query"]:
            publisher = release_date = None
            if options["publisher"]:
                publisher = options["publisher"]
            if options["date"]:
                release_date = options["date"]

            try:
                res = self.talker.query(publisher, None, None, release_date)
            except sb_err.ApiError as e:
                print(f"{e}")
                exit(0)

            if not res:
                self.stdout.write(self.style.ERROR("No results were available."))
                exit(0)

            new_list = clean_shortboxed_data(res)

            # Query the series name
            for item in new_list:
                series_name, issue_number = get_query_values(item)
                self.stdout.write(f"Searching database for {item.title}")
                results = Series.objects.filter(name__icontains=series_name)
                if results:
                    correct_series = select_list_choice(results)
                    if correct_series:
                        self.add_issue_to_database(correct_series, issue_number, item)
                    else:
                        self.stdout.write(
                            self.style.NOTICE(f"Not adding {item.title} to database.\n\n")
                        )
                else:
                    self.stdout.write(f"No series in database for {series_name}\n\n")
