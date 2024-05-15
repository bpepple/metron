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

        arcs = Arc.objects.filter(modified__date=search_date).exclude(edited_by=admin)
        characters = Character.objects.filter(modified__date=search_date).exclude(edited_by=admin)
        creators = Creator.objects.filter(modified__date=search_date).exclude(edited_by=admin)
        issues = Issue.objects.filter(modified__date=search_date).exclude(edited_by=admin)
        publishers = Publisher.objects.filter(modified__date=search_date).exclude(edited_by=admin)
        teams = Team.objects.filter(modified__date=search_date).exclude(edited_by=admin)

        title = f"Changes for {search_date}\n------------------------"

        self.stdout.write(self.style.SUCCESS(title))
        if arcs:
            self.stdout.write(self.style.SUCCESS("\nStory Arcs:"))
            for arc in arcs:
                self.stdout.write(self.style.WARNING(f"\t'{arc}' changed by '{arc.edited_by}'"))
        if characters:
            self.stdout.write(self.style.SUCCESS("\nCharacters:"))
            for character in characters:
                self.stdout.write(self.style.WARNING(f"\t'{character}' changed by '{character.edited_by}'"))
        if creators:
            self.stdout.write(self.style.SUCCESS("\nCreators:"))
            for creator in creators:
                self.stdout.write(self.style.WARNING(f"\t'{creator}' changed by '{creator.edited_by}'"))
        if issues:
            self.stdout.write(self.style.SUCCESS("\nIssues:"))
            for issue in issues:
                self.stdout.write(self.style.WARNING(f"\t'{issue}' changed by '{issue.edited_by}'"))
        if publishers:
            self.stdout.write(self.style.SUCCESS("\nPublishers:"))
            for publisher in publishers:
                self.stdout.write(self.style.WARNING(f"\t'{publisher}' changed by '{publisher.edited_by}'"))
        if teams:
            self.stdout.write(self.style.SUCCESS("\nTeams:"))
            for team in teams:
                self.stdout.write(self.style.WARNING(f"\t'{team}' changed by '{team.edited_by}'"))
