from datetime import datetime

from django.core.management.base import BaseCommand

from comicsdb.models import Arc, Character, Creator, Issue, Publisher, Team
from users.models import CustomUser


class Command(BaseCommand):
    help = "Show created / modified objects"

    def add_arguments(self, parser):
        """Add the arguments to the command."""
        parser.add_argument(
            "--date", type=str, required=True, help="Date string to search (yyyy-mm-dd)"
        )

    def handle(self, *args, **options):
        search_date = datetime.strptime(options["date"], "%Y-%m-%d").date()
        admin = CustomUser.objects.get(id=1)

        models = [Arc, Issue, Character, Creator, Team, Publisher]
        results: list[dict] = []
        for mod in models:
            qs_created = mod.objects.filter(modified__date=search_date).exclude(
                created_by=admin
            )
            qs_modified = mod.objects.filter(modified__date=search_date).exclude(
                edited_by=admin
            )
            qs = (qs_created | qs_modified).distinct()
            results.append({"model": mod, "qs": qs})

        if all(not v["qs"] for v in results):
            self.stdout.write(self.style.WARNING("No changes found."))
            return

        title = f"Changes for {search_date}\n-----------------------"
        self.stdout.write(self.style.SUCCESS(title))

        for item in results:
            if item["qs"]:
                self.stdout.write(self.style.SUCCESS(f"\n{item['model'].__name__}:"))
                for obj in item["qs"]:
                    user_str = (
                        f"{obj.edited_by}" if obj.edited_by != admin else f"{obj.created_by}"
                    )
                    self.stdout.write(
                        self.style.WARNING(f"\t'{obj}' created/changed by '{user_str}'")
                    )
