from datetime import datetime

import dateutil.relativedelta
from comicsdb.models import Issue, Series
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from ._sbtalker import ShortBoxedTalker
from ._utils import clean_shortboxed_data, select_series_choice


def get_query_values(item):
    name = item["title"].split("#")
    return name[0].strip(), name[1]


def format_string_to_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def determine_cover_date(release_date):
    new_date = release_date + dateutil.relativedelta.relativedelta(months=2)
    return new_date.replace(day=1)


def add_issue_to_database(series_obj, issue_number, sb_data):
    release_date = format_string_to_date(sb_data["release_date"])
    cover_date = determine_cover_date(release_date)

    c, _ = Issue.objects.get_or_create(
        series=series_obj,
        number=issue_number,
        slug=slugify(series_obj.slug + " " + issue_number),
        desc=sb_data["description"].strip(),
        store_date=release_date,
        cover_date=cover_date,
    )

    return c


class Command(BaseCommand):
    help = "Retrieve weekly comics from Shortboxed.com"

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
            self.stdout.write(f"Searching database for {series_name}")
            results = Series.objects.filter(name__icontains=series_name)
            if results:
                correct_series = select_series_choice(results)
                if correct_series:
                    issue = add_issue_to_database(correct_series, issue_number, item)
                    self.stdout.write(f"Add {issue} to database.")
                else:
                    self.stdout.write(
                        f"No correct series in databaser for {series_name}"
                    )
            else:
                self.stdout.write(f"No record found for '{series_name}'")
