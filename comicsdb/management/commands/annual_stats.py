from django.core.management.base import BaseCommand, CommandParser

from comicsdb.models import Arc, Character, Creator, Issue, Publisher, Series, Team
from users.models import CustomUser


class Command(BaseCommand):
    help = "Get annual stats for all comics"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("year", type=int, help="Year for stats.")
        return super().add_arguments(parser)

    def handle(self, *args: any, **options: any) -> None:
        users = CustomUser.objects.filter(date_joined__year=options["year"]).count()
        comics = Issue.objects.filter(created_on__year=options["year"]).count()
        characters = Character.objects.filter(created_on__year=options["year"]).count()
        creators = Creator.objects.filter(created_on__year=options["year"]).count()
        teams = Team.objects.filter(created_on__year=options["year"]).count()
        arcs = Arc.objects.filter(created_on__year=options["year"]).count()
        publishers = Publisher.objects.filter(created_on__year=options["year"]).count()
        series = Series.objects.filter(created_on__year=options["year"]).count()

        title = f"{options['year']} New Additions Statistics"
        self.stdout.write(self.style.SUCCESS(f"{title}\n{len(title) * '-'}"))
        self.stdout.write(
            self.style.SUCCESS(
                f"Users: {users:,}\n"
                f"Publishers: {publishers:,}\n"
                f"Series: {series:,}\n"
                f"Comics: {comics:,}\n"
                f"Characters: {characters:,}\n"
                f"Creators: {creators:,}\n"
                f"Teams: {teams:,}\n"
                f"Arcs: {arcs:,}\n"
            )
        )
