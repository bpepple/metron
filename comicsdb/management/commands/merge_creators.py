"""
PROCEED WITH CAUTION: uses deduplication fields to permanently merge Creator data objects
"""
from comicsdb.management.merge_command import MergeCommand
from comicsdb.models.creator import Creator


class Command(MergeCommand):
    """Merges two creators by ID"""

    help = "merges specified creators into one"

    MODEL = Creator
