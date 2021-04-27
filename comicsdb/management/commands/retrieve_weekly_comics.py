from comicsdb.models import Series
from django.core.management.base import BaseCommand

from ._sbtalker import ShortBoxedTalker
from ._utils import clean_shortboxed_data


def get_series_name(item):
    name = item["title"].split("#")
    return name[0].strip()


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
        res = sb.fetch_query_request(release_date, publisher)
        if not res:
            self.stdout.write(self.style.ERROR("No results were available."))
            exit(0)

        comics_list = sb.convert_json_to_list(res)
        new_list = clean_shortboxed_data(comics_list)

        # Query the series name
        for item in new_list:
            series_name = get_series_name(item)
            results = Series.objects.filter(name__icontains=series_name)
            if results:
                for item in results:
                    self.stdout.write(f"Found {item}")
            else:
                self.stdout.write(
                    self.style.SQL_KEYWORD(f"No record found for '{series_name}'")
                )
