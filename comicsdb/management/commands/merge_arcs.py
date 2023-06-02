"""
PROCEED WITH CAUTION: uses deduplication fields to permanently merge Arc data objects
"""
from comicsdb.management.merge_command import MergeCommand
from comicsdb.models.arc import Arc


class Command(MergeCommand):
    """merges two story arcs by ID"""

    help = "merges specified story arcs into one"

    MODEL = Arc
