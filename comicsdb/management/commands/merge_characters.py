"""
PROCEED WITH CAUTION: uses deduplication fields to permanently merge Character data objects
"""

from comicsdb.management.merge_command import MergeCommand
from comicsdb.models.character import Character


class Command(MergeCommand):
    """merges two characters by ID"""

    help = "merges specified characters into one"

    MODEL = Character
