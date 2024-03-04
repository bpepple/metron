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

        issues = Issue.objects.filter(created_on__month=month, created_on__year=year).count()
        users = CustomUser.objects.filter(
            date_joined__month=month, date_joined__year=year
        ).count()
        characters = Character.objects.filter(
            created_on__month=month, created_on__year=year
        ).count()
        creators = Creator.objects.filter(
            created_on__month=month, created_on__year=year
        ).count()

        title = f"Stats for {date(year, month, 1).strftime('%B %Y')}"

        self.stdout.write(self.style.SUCCESS(title))
        self.stdout.write(self.style.SUCCESS(f"{'-' * len(title)}"))
        self.stdout.write(self.style.SUCCESS(f"Users: {users}"))
        self.stdout.write(self.style.SUCCESS(f"Issues: {issues}"))
        self.stdout.write(self.style.SUCCESS(f"Creators: {creators}"))
        self.stdout.write(self.style.SUCCESS(f"Characters: {characters}"))
