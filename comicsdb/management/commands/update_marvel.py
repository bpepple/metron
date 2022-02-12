from decimal import Decimal
from typing import Any, Optional

import esak
from django.core.management.base import BaseCommand, CommandParser

from comicsdb.models.issue import Issue
from comicsdb.models.series import Series
from metron.settings import MARVEL_PRIVATE_KEY, MARVEL_PUBLIC_KEY

from ._utils import select_issue_choice


class Command(BaseCommand):
    help = "Update comic with information from the Marvel API."

    def _get_metron_issue_list(self, slug: str):
        series = Series.objects.get(slug=slug)
        return Issue.objects.filter(series=series)

    def _query_marvel_for_issue(self, title: str, number: int):
        m = esak.api(MARVEL_PUBLIC_KEY, MARVEL_PRIVATE_KEY)
        return sorted(
            m.comics_list(
                {
                    "format": "comic",
                    "formatType": "comic",
                    "noVariants": True,
                    "limit": 100,
                    "title": title,
                    "issueNumber": number,
                }
            ),
            key=lambda comic: comic.title,
        )

    def _check_for_solicit_txt(self, text_objects):
        return next((i.text for i in text_objects if i.type == "issue_solicit_text"), None)

    def _add_stories(self, stories):
        return [
            s.name
            for s in stories
            if s.type == "interiorStory"
            and not s.name.__contains__("story from")
            and not s.name.__contains__("interior to")
        ]

    def _update_issue(self, issue: Issue, marvel_data):
        modified = False

        if not issue.desc and marvel_data.text_objects:
            if solicit := self._check_for_solicit_txt(marvel_data.text_objects):
                issue.desc = solicit
                self.stdout.write(self.style.SUCCESS(f"Added description to {issue}."))
                modified = True

        if not issue.price and marvel_data.prices.print > Decimal("0.00"):
            issue.price = marvel_data.prices.print
            self.stdout.write(
                self.style.SUCCESS(f"Add price of '{marvel_data.prices.print}' to {issue}")
            )
            modified = True

        if not issue.upc and marvel_data.upc:
            issue.upc = marvel_data.upc
            self.stdout.write(
                self.style.SUCCESS(f"Added UPC of '{marvel_data.upc}' to {issue}.")
            )
            modified = True

        if not issue.page and marvel_data.page_count:
            issue.page = marvel_data.page_count
            self.stdout.write(self.style.SUCCESS(f"Added page count to {issue}."))
            modified = True

        if not issue.name and marvel_data.stories:
            if stories := self._add_stories(marvel_data.stories):
                issue.name = stories
                self.stdout.write(self.style.SUCCESS(f"Add titles to {issue}"))
                modified = True

        if modified:
            issue.save()
        else:
            self.stdout.write(self.style.NOTICE("No information needed to be updated."))

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-s", "--series", type=str, help="Series slug to query for.")
        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        if options["series"]:
            issues = self._get_metron_issue_list(options["series"])
            for i in issues:
                self.stdout.write(
                    self.style.HTTP_INFO(
                        f"\nSearching for {i.series.name} ({i.series.year_began}) #{i.number}"
                    )
                )
                if results := self._query_marvel_for_issue(i.series.name, int(i.number)):
                    if correct_issue := select_issue_choice(results):
                        self._update_issue(i, correct_issue)
                    else:
                        self.stdout.write(self.style.NOTICE(f"No match found for {i}.\n\n"))
                else:
                    self.stdout.write(self.style.NOTICE(f"No match found for {i}.\n\n"))

        else:
            self.stdout.write(self.style.NOTICE("No series given to query for."))
