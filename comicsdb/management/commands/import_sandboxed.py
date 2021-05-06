from comicsdb.models import Issue, Series
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.text import slugify

from ._sbtalker import ShortBoxedTalker
from ._utils import (clean_description, clean_shortboxed_data,
                     determine_cover_date, format_string_to_date,
                     get_query_values, select_series_choice)


class Command(BaseCommand):
    help = "Retrieve weekly comics from Shortboxed.com"

    def add_issue_to_database(self, series_obj, issue_number, sb_data):
        release_date = format_string_to_date(sb_data["release_date"])
        cover_date = determine_cover_date(release_date, sb_data["publisher"])
        clean_desc = clean_description(sb_data["description"])

        try:
            issue, create = Issue.objects.get_or_create(
                series=series_obj,
                number=issue_number,
                slug=slugify(series_obj.slug + " " + issue_number),
                desc=clean_desc.strip(),
                store_date=release_date,
                cover_date=cover_date,
            )

            if create:
                self.stdout.write(self.style.SUCCESS(f"Added {issue} to database.\n\n"))
            else:
                self.stdout.write(self.style.WARNING(f"{issue} already exists...\n\n"))
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(
                    f"{series_obj} #{issue_number} already existing in the database.\n\n"
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
            sb = ShortBoxedTalker()
            results = sb.fetch_available_releases()
            self.stdout.write(f"Last {NUMBER_OF_WEEKS} release dates:")
            for i in results["dates"][-NUMBER_OF_WEEKS:]:
                self.stdout.write(i)

        if options["query"]:
            publisher = release_date = None
            if options["publisher"]:
                publisher = options["publisher"]
            if options["date"]:
                release_date = options["date"]

            sb = ShortBoxedTalker()
            sb_results = sb.fetch_query_request(release_date, publisher)
            if not sb_results:
                self.stdout.write(self.style.ERROR("No results were available."))
                exit(0)

            comics_list = sb.convert_json_to_list(sb_results)
            new_list = clean_shortboxed_data(comics_list)

            # Query the series name
            for item in new_list:
                series_name, issue_number = get_query_values(item)
                self.stdout.write(f"Searching database for {item['title']}")
                results = Series.objects.filter(name__icontains=series_name)
                if results:
                    correct_series = select_series_choice(results)
                    if correct_series:
                        self.add_issue_to_database(correct_series, issue_number, item)
                    else:
                        self.stdout.write(
                            self.style.NOTICE(
                                f"Not adding {item['title']} to database.\n\n"
                            )
                        )
                else:
                    self.stdout.write(f"No series in database for {series_name}\n\n")
