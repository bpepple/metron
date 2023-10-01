"""
PROCEED WITH CAUTION: uses deduplication fields to permanently merge Publisher data objects
"""
from comicsdb.management.merge_command import MergeCommand
from comicsdb.models.publisher import Publisher


class Command(MergeCommand):
    """Merges two publishers by ID"""

    help = "Merges specified teams into one"

    MODEL = Publisher
