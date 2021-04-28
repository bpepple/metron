from comicsdb.models import Issue, Series
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from ._sbtalker import ShortBoxedTalker
from ._utils import (
    clean_description,
    clean_shortboxed_data,
    determine_cover_date,
    format_string_to_date,
    get_query_values,
    select_series_choice,
)


class Command(BaseCommand):
    help = "Retrieve weekly comics from Shortboxed.com"

    def add_issue_to_database(self, series_obj, issue_number, sb_data):
        release_date = format_string_to_date(sb_data["release_date"])
        cover_date = determine_cover_date(release_date, sb_data["publisher"])
        clean_desc = clean_description(sb_data["description"])

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

    def add_arguments(self, parser):
        parser.add_argument(
            "-p", "--publisher", type=str, help="The publisher to query"
        )
        parser.add_argument(
            "-d", "--date", type=str, help="Enter a release date in YYYY-MM-DD format"
        )

    def handle(self, *args, **options):
        if not options["date"] or not options["publisher"]:
            self.stdout.write(
                self.style.ERROR("Missing publisher or date query values.")
            )
            exit(0)

        publisher = options["publisher"]
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
                    self.stdout.write(self.style.NOTICE(f"Not adding {item['title']} to database.\n\n"))
            else:
                self.stdout.write(f"No series in database for {series_name}\n\n")
