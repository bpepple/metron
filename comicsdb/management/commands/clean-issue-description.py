from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from comicsdb.models import Series
from comicsdb.models.issue import Issue


class Command(BaseCommand):
    help = "Clean issue descriptions."

    @staticmethod
    def _clean_desc(txt: str) -> str:
        split_txt = txt.split("\n\n")
        split_len = len(split_txt)
        if split_len > 1:
            if split_txt[-1].lower().startswith("content"):
                return "\n\n".join(split_txt[:-1]) if split_len > 2 else split_txt[0]
            else:
                return txt
        return txt

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--series", type=int, required=True)
        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> None:
        series = Series.objects.get(id=options["series"])
        print(series)
        issues = Issue.objects.filter(series=series)
        for i in issues:
            i.desc = self._clean_desc(i.desc)
        Issue.objects.bulk_update(issues, ["desc"], batch_size=250)
