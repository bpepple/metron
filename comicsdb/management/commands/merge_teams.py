"""
PROCEED WITH CAUTION: uses deduplication fields to permanently merge Team data objects
"""

from comicsdb.management.merge_command import MergeCommand
from comicsdb.models.team import Team


class Command(MergeCommand):
    """Merges two teams by ID"""

    help = "Merges specified teams into one"

    MODEL = Team
