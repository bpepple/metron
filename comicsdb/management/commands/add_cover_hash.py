from typing import Any

import imagehash
from django.core.management.base import BaseCommand, CommandParser
from PIL import Image

from comicsdb.models.issue import Issue


class Command(BaseCommand):
    help = "Add missing cover hashes"

    def add_arguments(self, parser: CommandParser) -> None:
        """add the arguments for this command"""
        parser.add_argument(
            "--batch",
            type=int,
            required=False,
            default=250,
            help="Number of issues to do in bulk_update. Default: 250",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        missing_count = Issue.objects.all().exclude(image="").filter(cover_hash="").count()
        print(f"Bath: {options['batch']}")
        while missing_count > 0:
            issues = Issue.objects.exclude(image="").filter(cover_hash="")[: options["batch"]]
            for i in issues:
                try:
                    cover_hash = imagehash.phash(Image.open(i.image))
                except OSError as e:
                    print(f"Skipping {i}. Error: {e}")
                    continue
                i.cover_hash = str(cover_hash)
                print(f"Set cover hash of '{cover_hash}' for '{i}'")

            update_count = Issue.objects.bulk_update(issues, ["cover_hash"])
            print(f"Updated {update_count} issues in the database")
            missing_count = missing_count - update_count
