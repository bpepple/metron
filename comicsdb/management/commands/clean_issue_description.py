from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from comicsdb.models import Series
from comicsdb.models.issue import Issue


class Command(BaseCommand):
    help = "Clean issue descriptions."

    @staticmethod
    def _clean_desc(txt: str) -> str:
        two_paragraphs = 2
        # No text, let's bail.
        if not txt:
            return ""
        split_txt = txt.split("\n\n")
        split_len = len(split_txt)
        # If the description starts with a bad value let's return an empty string.
        if split_len < two_paragraphs and (
            split_txt[0].lower().startswith(("content", "note", "story", "chapter", "synopsis"))
        ):
            return ""
        # If there are 2 or more paragraphs, loop through them looking for a bad starting
        # word and if so let's not join it to the return string.
        if split_len > 1:
            for idx, i in enumerate(split_txt):
                if (
                    str(i)
                    .strip("\n")
                    .lower()
                    .startswith(("content", "note", "story", "chapter", "synopsis"))
                ):
                    return (
                        "\n\n".join(split_txt[:idx]) if split_len > two_paragraphs else split_txt[0]
                    )

            return txt
        return txt

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--series", type=int, required=True)
        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> None:
        series = Series.objects.get(id=options["series"])
        print(f"Updating: {series}")
        issues = Issue.objects.filter(series=series)
        for i in issues:
            i.desc = self._clean_desc(i.desc)
        Issue.objects.bulk_update(issues, ["desc"], batch_size=100)
