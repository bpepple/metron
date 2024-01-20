from django.core.management.base import BaseCommand

from comicsdb.models import Issue, Universe


class Command(BaseCommand):
    help = "Add Universe to Series Issues"

    def add_arguments(self, parser):
        """add the arguments for this command"""
        parser.add_argument("--series", type=int, required=True)
        parser.add_argument("--universe", type=int, required=True)

    def handle(self, *args, **options):
        issues = Issue.objects.filter(series__id=options["series"])
        universe = Universe.objects.get(id=options["universe"])
        for issue in issues:
            if universe in issue.universes.all():
                self.stdout.write(self.style.WARNING(f"'{universe}' is already in '{issue}'"))
                continue
            issue.universes.add(universe)
            self.stdout.write(self.style.SUCCESS(f"Added '{universe}' to '{issue}'"))
