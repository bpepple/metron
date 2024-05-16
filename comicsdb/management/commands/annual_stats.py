from django.core.management.base import BaseCommand, CommandParser

from comicsdb.models import Arc, Character, Creator, Issue, Publisher, Series, Team
from users.models import CustomUser


class Command(BaseCommand):
    help = "Get annual stats for all comics"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("year", type=int, help="Year for stats.")
        return super().add_arguments(parser)

    def handle(self, *args: any, **options: any) -> None:
        results: list[dict] = []
        users = CustomUser.objects.filter(date_joined__year=options["year"]).count()
        results.append({"model": CustomUser, "count": users})

        models = [Arc, Character, Creator, Issue, Publisher, Series, Team]
        for mod in models:
            count = mod.objects.filter(created_on__year=options["year"]).count()
            results.append({"model": mod, "count": count})

        title = f"{options['year']} New Additions Statistics"
        self.stdout.write(self.style.SUCCESS(f"{title}\n{len(title) * '-'}"))
        for result in results:
            self.stdout.write(self.style.WARNING(f"{result['model'].__name__}: {result['count']:,}"))
