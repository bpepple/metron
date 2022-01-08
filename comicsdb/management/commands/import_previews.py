import csv
import platform
from datetime import datetime
from decimal import Decimal, DecimalException
from typing import List

import requests
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.text import slugify

from comicsdb.models.issue import Issue
from comicsdb.models.series import Series

from ._utils import (
    clean_shortboxed_data,
    determine_cover_date,
    get_query_values,
    select_list_choice,
)


class PreviewComic:
    def __init__(self) -> None:
        self.publisher: str = None
        self.sku: str = None
        self.title: str = None
        self.price: Decimal = 0.00


class Command(BaseCommand):
    def __init__(self) -> None:
        super().__init__()
        self.api_url = "https://www.previewsworld.com/NewReleases/Export"

    def add_arguments(self, parser):
        parser.add_argument(
            "-d",
            "--date",
            type=str,
            help="Enter a release date in MM/DD/YYYY format. Ex. 12/08/2021",
        )

    def add_issue_to_database(self, series_obj, issue_number, release, previews_data):
        cover_date = determine_cover_date(release, previews_data.publisher)
        try:
            issue, create = Issue.objects.get_or_create(
                series=series_obj,
                number=issue_number,
                slug=slugify(series_obj.slug + " " + issue_number),
                store_date=release,
                cover_date=cover_date,
            )

            modified = False
            if not issue.sku and previews_data.sku:
                issue.sku = previews_data.sku
                self.stdout.write(
                    self.style.SUCCESS(f"Added sku of '{previews_data.sku}' to {issue}.")
                )
                modified = True

            if not issue.price and previews_data.price:
                issue.price = previews_data.price
                self.stdout.write(
                    self.style.SUCCESS(f"Added price of ${issue.price} to {issue}.")
                )
                modified = True

            if modified:
                issue.save()

            if create:
                self.stdout.write(self.style.SUCCESS(f"Added {issue} to database.\n\n"))
            else:
                self.stdout.write(self.style.WARNING(f"{issue} already exists...\n\n"))
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(
                    f"Integrity Error: {series_obj} #{issue_number} already existing in the database.\n\n"
                )
            )

    def _retrieve_data(self, date: str):
        params = {"format": "text", "releaseDate": date}
        header = {"User-Agent": f"metron ({platform.system()}; {platform.release()})"}
        response = requests.get(self.api_url, params=params, headers=header)
        response.raise_for_status()

        return response

    def _remove_intro_text(self, txt):
        lines = []
        lines = txt.strip().splitlines()

        return [line for number, line in enumerate(lines) if number not in range(9)]

    def _remove_empty_items(self, lst):
        return [i for i in lst if i]

    def _check_valid_publisher(self, publisher):
        valid = [
            "BOOM! STUDIOS",
            "DARK HORSE COMICS",
            "DYNAMITE",
            "IDW PUBLISHING",
            "IMAGE COMICS",
            "MARVEL COMICS",
        ]
        return publisher in valid

    def _is_decimal(self, string: str) -> bool:
        try:
            Decimal(string)
            return True
        except (ValueError, DecimalException):
            return False

    def _convert_price(self, price: str) -> Decimal:
        new_val = price.strip("$")
        if not self._is_decimal(new_val):
            return Decimal("0.00")
        else:
            return Decimal(new_val)

    def _check_if_variant(self, comic):
        var_list = [
            "VAR",
            "CVR B",
            "CVR C",
            "CVR D",
            "CVR E",
            "CVR F",
            "CVR G",
            "CVR H",
            "CVR I",
            "CVR J",
            "CVR K",
            "CVR L",
            "CVR M",
            "CVR N",
            "CVR O",
            "CVR P",
            "CVR Q",
            "CVR R",
            "CVR S",
            "CVR T",
            "CVR U",
            "CVR V",
            "CVR W",
            "CVR X",
            "CVR Y",
            "CVR Z",
            "TP",
            "HC",
            "POSTER",
            "LITHO",
            "GN",
            "BLOODY LOGO",
            "TRADING CARDS",
        ]
        return any(i in comic.title for i in var_list)

    def _set_comic(self, pub, row):
        comic = PreviewComic()
        comic.publisher = pub
        comic.sku = row[0]
        comic.title = row[1]
        comic.price = self._convert_price(row[2])
        return comic

    def _process_cvs(self, readCVS):
        lst: List[PreviewComic] = []
        pub = None
        for row in readCVS:
            if len(row) < 2:
                pub = row[0]
                valid = self._check_valid_publisher(pub)
                continue
            if valid:
                comic = self._set_comic(pub, row)
                if not self._check_if_variant(comic):
                    lst.append(comic)
        return lst

    def handle(self, *args, **options):
        if not options["date"]:
            self.stdout.write(self.style.NOTICE("No date given requested. Exiting..."))
            exit(0)

        resp = self._retrieve_data(options["date"])
        res = self._remove_intro_text(resp.text)
        res = self._remove_empty_items(res)

        readCVS = csv.reader(res, delimiter=",")
        lst = self._process_cvs(readCVS)
        lst = clean_shortboxed_data(lst)

        release_date = datetime.strptime(options["date"], "%m/%d/%Y").date()
        for item in lst:
            series_name, issue_number = get_query_values(item)
            # print(f"{series_name} #{issue_number}")
            self.stdout.write(f"Searching database for {item.title}")
            results = Series.objects.filter(name__icontains=series_name)
            if results:
                correct_series = select_list_choice(results)
                if correct_series:
                    self.add_issue_to_database(
                        correct_series, issue_number, release_date, item
                    )
                else:
                    self.stdout.write(
                        self.style.NOTICE(f"Not adding {item.title} to database.\n\n")
                    )
            else:
                self.stdout.write(f"No series in database for {series_name}\n\n")
