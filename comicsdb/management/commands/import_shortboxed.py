from decimal import Decimal

import serifan
from comicsdb.models import Issue, Series
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.text import slugify
from simple_history.utils import update_change_reason

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
        self.talker = serifan.api()

    def _fix_price(self, price):
        fixed = price.strip("$")
        return Decimal(fixed)

    def add_issue_to_database(self, series_obj, issue_number, sb_data):
        cover_date = determine_cover_date(sb_data.release_date, sb_data.publisher)
        price = self._fix_price(sb_data.price)
        try:
            issue, create = Issue.objects.get_or_create(
                series=series_obj,
                number=issue_number,
                slug=slugify(series_obj.slug + " " + issue_number),
                store_date=sb_data.release_date,
                cover_date=cover_date,
                price=price,
                sku=sb_data.diamond_id,
            )
            clean_desc = clean_description(sb_data.description)

            if create:
                issue.desc = clean_desc.strip()
                issue.save()
                # Save the change reason
                update_change_reason(issue, "Shortboxed import")
                self.stdout.write(self.style.SUCCESS(f"Added {issue} to database.\n\n"))
            elif not issue.desc and clean_desc:
                # If an issue already exists and doesn't have a description, let's add one.
                issue.desc = clean_desc.strip()
                issue.save()
                # Save the change reason
                update_change_reason(issue, "Shortboxed import")
                self.stdout.write(
                    self.style.SUCCESS(f"Adding description to {issue}\n\n")
                )
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
        parser.add_argument(
            "-p", "--publisher", type=str, help="The publisher to query"
        )
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

            res = self.talker.query(publisher, None, None, release_date)
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
                            self.style.NOTICE(
                                f"Not adding {item.title} to database.\n\n"
                            )
                        )
                else:
                    self.stdout.write(f"No series in database for {series_name}\n\n")
