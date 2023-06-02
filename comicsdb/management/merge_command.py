from django.core.management.base import BaseCommand

from comicsdb.management.merge import merge_objects


class MergeCommand(BaseCommand):
    """base class for merge commands"""

    def add_arguments(self, parser):
        """add the arguments for this command"""
        parser.add_argument("--canonical", type=int, required=True)
        parser.add_argument("--other", type=int, required=True)

    # pylint: disable=no-self-use,unused-argument
    def handle(self, *args, **options):
        """merge the two objects"""
        model = self.MODEL

        try:
            canonical = model.objects.get(id=options["canonical"])
        except model.DoesNotExist:
            print(f"{model.__name__} doesn’t exist!")
            return
        try:
            other = model.objects.get(id=options["other"])
        except model.DoesNotExist:
            print(f"Other {model.__name__} doesn’t exist!")
            return

        merge_objects(canonical, other)
