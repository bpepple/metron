from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional

import esak
from django.core.management.base import BaseCommand
from esak.exceptions import ApiError

from comicsdb.models.issue import Issue
from comicsdb.models.series import Series
from metron.settings import MARVEL_PRIVATE_KEY, MARVEL_PUBLIC_KEY

from ._utils import select_issue_choice


class Command(BaseCommand):
    help = "Update comic with information from the Marvel API."

    def _get_metron_issue_list(self, slug: str, cover: Optional[date]):
        series = Series.objects.get(slug=slug)
        if cover:
            return Issue.objects.filter(series=series, cover_date__gte=cover)
        else:
            return Issue.objects.filter(series=series)

    def _query_marvel_for_issue(self, title: str, number: int):
        try:
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
        except ApiError:
            return None

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

    def _cleanup_upc(self, upc: str) -> str:
        return upc.replace("-", "")

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
            upc = self._cleanup_upc(marvel_data.upc)
            issue.upc = upc
            self.stdout.write(self.style.SUCCESS(f"Added UPC of '{upc}' to {issue}."))
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

    def _ask_if_want_to_search(self, i: Issue) -> bool:
        self.stdout.write(
            self.style.HTTP_INFO(
                f"\nDo you want to search for {i.series.name} ({i.series.year_began}) #{i.number} ({i.cover_date})"
            )
        )
        while True:
            i = input("Choose (Y)es or (N)o: ")
            if i.isalpha():
                break

        return i.lower() == "y"

    def _ask_for_series_slug(self):
        while True:
            i = input("Enter slug of series to search for, or q to quit: ")
            if isinstance(i, str) or i.lower() == "q":
                break

        return i if i != "q" else exit(0)

    def _ask_for_cover_date(self) -> Optional[date]:
        while True:
            i = input(
                "Enter issue cover date to start with (e.g. 2013-01-01), or n for None: "
            )
            if isinstance(i, str) or i.lower() == "n":
                break

        return datetime.strptime(i, "%Y-%m-%d") if i != "n" else None

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        slug = self._ask_for_series_slug()
        if cover := self._ask_for_cover_date():
            issues = self._get_metron_issue_list(slug, cover)
        else:
            issues = self._get_metron_issue_list(slug, None)

        for i in issues:
            self.stdout.write(
                self.style.HTTP_INFO(
                    f"\nSearching for {i.series.name} ({i.series.year_began}) #{i.number} ({i.cover_date})"
                )
            )
            if not i.number.isnumeric():
                self.stdout.write(self.style.WARNING(f"Unsupported issue number: {i.number}"))
                continue

            if results := self._query_marvel_for_issue(i.series.name, int(i.number)):
                if correct_issue := select_issue_choice(results):
                    self._update_issue(i, correct_issue)
                else:
                    self.stdout.write(self.style.NOTICE(f"No match found for {i}.\n"))
            else:
                self.stdout.write(self.style.NOTICE(f"No match found for {i}.\n"))
