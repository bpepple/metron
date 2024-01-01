from django.core.management.base import BaseCommand, CommandParser

from comicsdb.models import Character, Creator, Issue
from users.models import CustomUser


class Command(BaseCommand):
    help = "Get annual stats for all comics"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("year", type=int, help="Year for stats.")
        return super().add_arguments(parser)

    def handle(self, *args: any, **options: any) -> None:
        year_comics = Issue.objects.filter(created_on__year=options["year"]).count()
        year_users = CustomUser.objects.filter(date_joined__year=options["year"]).count()
        year_characters = Character.objects.filter(created_on__year=options["year"]).count()
        year_creators = Creator.objects.filter(created_on__year=options["year"]).count()

        title = f"{options['year']} Statistics"
        print(f"{title}\n{len(title) * '-'}")
        print(
            f"New Comics: {year_comics}\nNew Users: {year_users}\n"
            f"New Characters: {year_characters}\nNew Creators: {year_creators}"
        )
