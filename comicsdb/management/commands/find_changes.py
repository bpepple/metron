from django.core.management.base import BaseCommand
from datetime import datetime

from comicsdb.models import Arc, Issue, Character, Creator, Team, Publisher
from users.models import CustomUser


class Command(BaseCommand):
    help = "Show created / modified objects"

    def add_arguments(self, parser):
        """Add the arguments to the command."""
        parser.add_argument("--date", type=str, required=True, help="Date string to search (yyyy-mm-dd)")

    def handle(self, *args, **options):
        search_date = datetime.strptime(options["date"], "%Y-%m-%d").date()
        admin = CustomUser.objects.get(id=1)

        models = [Arc, Issue, Character, Creator, Team, Publisher]
        results: list[dict] = []
        for mod in models:
            qs = mod.objects.filter(modified__date=search_date).exclude(edited_by=admin)
            results.append({"model": mod, "queryset": qs})

        title = f"Changes for {search_date}\n-----------------------"
        self.stdout.write(self.style.SUCCESS(title))

        for item in results:
            if item["queryset"]:
                self.stdout.write(self.style.SUCCESS(f"\n{item['model'].__name__}:"))
                for obj in item["queryset"]:
                    self.stdout.write(self.style.WARNING(f"\t'{obj}' changed by '{obj.edited_by}'"))
