from django.core.management.base import BaseCommand
from django.utils.text import slugify

from comicsdb.models import Issue, Series


class Command(BaseCommand):
    help = "Fix series start year"

    def add_arguments(self, parser) -> None:
        parser.add_argument("--series", type=int, required=True, help="Series ID number")
        parser.add_argument("--year", type=int, required=True)

    def handle(self, *args, **options) -> None:
        series = Series.objects.get(pk=options["series"])
        series.year_began = options["year"]
        series.slug = slugify(f"{series.name}-{series.year_began}")
        series.save()
        self.stdout.write(self.style.SUCCESS(f"Update start year for {series}"))

        qs = Issue.objects.filter(series=series)
        for issue in qs:
            issue.slug = slugify(f"{series.slug}-{issue.number}")

        res = Issue.objects.bulk_update(qs, ["slug"])
        self.stdout.write(self.style.SUCCESS(f"Successfully change the slug for {res} issues"))
