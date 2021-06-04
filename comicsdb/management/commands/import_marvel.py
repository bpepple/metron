import shutil
import tempfile
from datetime import datetime
from os import fspath
from pathlib import Path
from urllib.request import urlopen

import dateutil.relativedelta
import marvelous
from boto3 import session
from boto3.s3.transfer import S3Transfer
from comicsdb.models import Character, Creator, Credits, Issue, Role, Series
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.text import slugify
from metron.settings import DEBUG, MARVEL_PRIVATE_KEY, MARVEL_PUBLIC_KEY
from metron.storage_backends import MediaStorage
from simple_history.utils import update_change_reason

from ._parse_title import FileNameParser
from ._utils import select_series_choice

if not DEBUG:
    from metron.settings import (
        AWS_ACCESS_KEY_ID,
        AWS_S3_ENDPOINT_URL,
        AWS_SECRET_ACCESS_KEY,
        AWS_STORAGE_BUCKET_NAME,
    )
else:
    from metron.settings import MEDIA_ROOT


class Command(BaseCommand):
    help = "Retrieve next months comics from the Marvel API."

    @property
    def get_upload_image_path(self):
        now = datetime.now()
        return f"issue/{now:%Y/%m/%d}/"

    def _upload_image(self, image):
        # TODO: Should probably use Storage to upload image instead of boto directly
        media_storage = MediaStorage()
        upload_file = (
            f"{media_storage.location}/{self.get_upload_image_path}{image.name}"
        )

        sesh = session.Session()
        client = sesh.client(
            "s3",
            region_name="nyc3",
            endpoint_url=AWS_S3_ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        transfer = S3Transfer(client)
        transfer.upload_file(
            str(image),
            AWS_STORAGE_BUCKET_NAME,
            upload_file,
            extra_args={"CacheControl": "max-age=604800", "ACL": "public-read"},
        )
        self.stdout.write(self.style.SUCCESS(f"Uploaded {image.name} to DigitalOcean."))

    def _fix_role(self, role):
        if role == "penciler":
            return "penciller"
        elif "cover" in role:
            return "cover"
        else:
            return role

    def _add_characters(self, marvel_data, issue_obj):
        for character in marvel_data.characters:
            try:
                c = Character.objects.get(name__iexact=character.name)
                issue_obj.characters.add(c)
            except Character.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Unable to find '{character.name}'. Skipping..."
                    )
                )
                continue

    def _add_creators(self, marvel_data, issue_obj):
        for creator in marvel_data.creators:
            try:
                c = Creator.objects.get(name__iexact=creator.name)
                r = self._fix_role(creator.role)
                role = Role.objects.get(name__iexact=r)
                credits = Credits.objects.create(issue=issue_obj, creator=c)
                credits.role.add(role)
                self.stdout.write(
                    self.style.SUCCESS(f"Add {c} as a {role} to {issue_obj}")
                )
            except Creator.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"Unable to find {creator.name}. Skipping...")
                )
                continue

    def _add_eic_credit(self, issue_obj):
        cb = Creator.objects.get(slug="c-b-cebulski")
        cr, create = Credits.objects.get_or_create(issue=issue_obj, creator=cb)
        self.stdout.write(self.style.SUCCESS(f"Added credit for {cb} to {issue_obj}."))
        if create:
            eic = Role.objects.get(name__iexact="editor in chief")
            cr.role.add(eic)
            self.stdout.write(
                self.style.SUCCESS(f"Added '{eic}' role for {cb} to {issue_obj}.")
            )

    def _download_image(self, url):
        url_path = Path(url)
        save_path = Path(tempfile.gettempdir()) / url_path.name
        with open(save_path, "wb") as img_file:
            img_file.write(urlopen(url).read())
        return save_path

    def _determine_cover_date(self, release_date):
        new_date = release_date + dateutil.relativedelta.relativedelta(months=2)
        return new_date.replace(day=1)

    def add_issue_to_database(
        self, series_obj, fnp: FileNameParser, marvel_data, cover: bool
    ):
        cover_date = self._determine_cover_date(marvel_data.dates.on_sale)
        slug = slugify(series_obj.slug + " " + fnp.issue)

        try:
            issue, create = Issue.objects.get_or_create(
                series=series_obj,
                number=fnp.issue,
                slug=slug,
                store_date=marvel_data.dates.on_sale,
                cover_date=cover_date,
            )
            if marvel_data.description:
                issue.desc = marvel_data.description
                issue.save()

            if create:
                if cover:
                    if not DEBUG:
                        self._get_cover(marvel_data, issue)
                    else:
                        self._get_cover_debug(marvel_data, issue)
                self._add_eic_credit(issue)
                if marvel_data.creators:
                    self._add_creators(marvel_data, issue)
                if marvel_data.characters:
                    self._add_characters(marvel_data, issue)
                # Save the change reason
                update_change_reason(issue, "Marvel import")
                self.stdout.write(self.style.SUCCESS(f"Added {issue} to database.\n\n"))
            else:
                if cover:
                    if not issue.image:
                        if not DEBUG:
                            self._get_cover(marvel_data, issue)
                        else:
                            self._get_cover_debug(marvel_data, issue)
                        self.stdout.write(
                            self.style.SUCCESS(f"Added image to {issue}\n")
                        )
                        # Save the change reason
                        update_change_reason(issue, "Imported")
                    else:
                        self.stdout.write(
                            self.style.WARNING(f"{issue} already exists...\n\n")
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"{issue} already exists...\n\n")
                    )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(
                    f"{series_obj} #{fnp.issue} already existing in the database.\n\n"
                )
            )

    def _get_cover_debug(self, marvel_data, issue):
        fn = self._download_image(marvel_data.images[0])
        issue.image = f"{self.get_upload_image_path}{fn.name}"
        issue.save()

        dest = Path(MEDIA_ROOT) / f"{self.get_upload_image_path}"
        if not dest.is_dir():
            dest.mkdir(parents=True)
        shutil.move(fspath(fn), fspath(dest))

    def _get_cover(self, marvel_data, issue):
        fn = self._download_image(marvel_data.images[0])
        issue.image = f"{self.get_upload_image_path}{fn.name}"
        issue.save()
        self._upload_image(fn)
        fn.unlink()

    def _get_data_from_marvel(self, options):
        m = marvelous.api(MARVEL_PUBLIC_KEY, MARVEL_PRIVATE_KEY)
        return sorted(
            m.comics(
                {
                    "format": "comic",
                    "formatType": "comic",
                    "noVariants": True,
                    "dateDescriptor": options["date"],
                    "limit": 100,
                }
            ),
            key=lambda comic: comic.title,
        )

    def add_arguments(self, parser):
        parser.add_argument(
            "-d",
            "--date",
            type=str,
            default="nextWeek",
            help="The date period to query.",
        )
        parser.add_argument(
            "-c",
            "--cover",
            help="Retrieve issue covers from Marvel.",
            action="store_true",
            default=False,
        )

    def handle(self, *args, **options):
        if not options["date"]:
            self.stdout.write(self.style.NOTICE("No month requested. Exiting..."))
            exit(0)

        pulls = self._get_data_from_marvel(options)

        fnp = FileNameParser()
        for comic in pulls:
            fnp.parse_filename(comic.title)
            self.stdout.write(f"Searching database for {fnp.series} #{fnp.issue}")
            results = Series.objects.filter(
                name__icontains=fnp.series, year_began=int(fnp.year)
            )
            if results:
                correct_series = select_series_choice(results)
                if correct_series:
                    self.add_issue_to_database(
                        correct_series, fnp, comic, options["cover"]
                    )
                else:
                    self.stdout.write(
                        self.style.NOTICE(
                            f"Not adding {fnp.series} #{fnp.issue} to database.\n\n"
                        )
                    )
            else:
                self.stdout.write(f"No series in database for {fnp.series}\n\n")
