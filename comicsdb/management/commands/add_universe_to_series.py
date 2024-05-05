from django.core.management.base import BaseCommand

from comicsdb.models import Issue, Universe


class Command(BaseCommand):
    help = "Add Universe to Series Issues"

    def add_arguments(self, parser):
        """add the arguments for this command"""
        parser.add_argument("--series", type=int, required=True)
        parser.add_argument("--universe", type=int, required=True)
        parser.add_argument(
            "--characters", action="store_true", help="Add characters to Universe."
        )

    def handle(self, *args, **options):
        issues = Issue.objects.filter(series__id=options["series"])
        universe = Universe.objects.get(id=options["universe"])
        for issue in issues:
            if universe not in issue.universes.all():
                issue.universes.add(universe)
                self.stdout.write(self.style.SUCCESS(f"Added '{universe}' to '{issue}'"))
            if options["characters"]:
                for character in issue.characters.all():
                    if universe in character.universes.all():
                        continue
                    character.universes.add(universe)
                    self.stdout.write(self.style.SUCCESS(f"Added '{universe}' to '{character}'"))
