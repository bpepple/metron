from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from comicsdb.models.credits import Credits, Role


class Command(BaseCommand):
    help = "Change 'Artist' role to 'Illustrator' for a series"

    def add_arguments(self, parser: CommandParser) -> None:
        """Add command arguments."""
        parser.add_argument(
            "--slug", type=str, required=True, help="Series slug for credits to be fixed"
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        artist = Role.objects.get(name="Artist")
        illustrator = Role.objects.get(name="Illustrator")
        qs = Credits.objects.filter(issue__series__slug=options["slug"])
        for i in qs:
            if artist in i.role.all():
                i.role.add(illustrator)
                i.role.remove(artist)
                self.stdout.write(
                    self.style.SUCCESS(f"Fixed role for {i.creator} in {i.issue}")
                )
