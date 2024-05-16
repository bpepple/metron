from datetime import date

from django.core.management.base import BaseCommand

from comicsdb.models import Character, Creator, Issue
from users.models import CustomUser


class Command(BaseCommand):
    help = "Get monthly stats"

    def add_arguments(self, parser: any) -> None:
        """Add the arguments to the command"""
        parser.add_argument("--month", type=int, required=True)
        parser.add_argument("--year", type=int, required=True)

    def handle(self, *args: any, **options: any) -> None:
        """Run the command"""
        month = options["month"]
        year = options["year"]
        results: list[dict] = []

        users = CustomUser.objects.filter(date_joined__month=month, date_joined__year=year).count()
        results.append({"model": CustomUser, "count": users})

        models = [Character, Creator, Issue]
        for mod in models:
            count = mod.objects.filter(created_on__month=month, created_on__year=year).count()
            results.append({"model": mod, "count": count})

        title = f"Stats for {date(year, month, 1).strftime('%B %Y')}"

        self.stdout.write(self.style.SUCCESS(title))
        self.stdout.write(self.style.SUCCESS(f"{'-' * len(title)}"))
        for result in results:
            self.stdout.write(self.style.WARNING(f"{result['model'].__name__}: {result['count']:,}"))
