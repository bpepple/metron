from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandParser

from comicsdb.models import Series
from comicsdb.models.credits import Credits, Role


class Command(BaseCommand):
    help = "Fix old anthology roles"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("slug", nargs="+", type=str)
        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        series = Series.objects.get(slug=options["slug"][0])
        qs = Credits.objects.filter(issue__series=series)
        pencil = Role.objects.get(name__iexact="penciller")
        ink = Role.objects.get(name__iexact="inker")
        artist = Role.objects.get(name__iexact="artist")
        writer = Role.objects.get(name__iexact="writer")
        story = Role.objects.get(name__iexact="story")

        for i in qs:
            fix = False
            # Fix writing credits.
            if writer in i.role.all():
                fix = True
                i.role.remove(writer)
                if story not in i.role.all():
                    i.role.add(story)
                print(f"Fixed writing role in {i.issue} for {i.creator}")

            # Fix art credits
            if pencil in i.role.all() and ink in i.role.all():
                fix = True
                i.role.remove(pencil)
                i.role.remove(ink)
                if artist not in i.role.all():
                    i.role.add(artist)
                print(f"Fixed artist credit in {i.issue} for {i.creator}")

            if not fix:
                print(f"Nothing to fix in {i.issue} for {i.creator}")
