import tempfile
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

import dateutil.relativedelta
import marvelous
from boto3 import session
from boto3.s3.transfer import S3Transfer
from comicsdb.models import Issue, Series
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.text import slugify
from metron.settings import DEBUG, MARVEL_PRIVATE_KEY, MARVEL_PUBLIC_KEY
from metron.storage_backends import MediaStorage

from ._parse_title import FileNameParser
from ._utils import select_series_choice

if not DEBUG:
    from metron.settings import (
        AWS_ACCESS_KEY_ID,
        AWS_S3_ENDPOINT_URL,
        AWS_SECRET_ACCESS_KEY,
        AWS_STORAGE_BUCKET_NAME,
    )


class Command(BaseCommand):
    help = "Retrieve next months comics from the Marvel API."

    @property
    def get_upload_image_path(self):
        now = datetime.now()
        return f"issue/{now:%Y/%m/%d}/"

    def _upload_image(self, image):
        media_storage = MediaStorage()
        upload_file = f"{media_storage.location}/{self.get_upload_image_path}{image.name}"

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

    def _download_image(self, url):
        url_path = Path(url)
        save_path = Path(tempfile.gettempdir()) / url_path.name
        with open(save_path, "wb") as img_file:
            img_file.write(urlopen(url).read())
        return save_path

    def _determine_cover_date(self, release_date):
        new_date = release_date + dateutil.relativedelta.relativedelta(months=2)
        return new_date.replace(day=1)

    def add_issue_to_database(self, series_obj, fnp: FileNameParser, marvel_data):
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
                if not DEBUG:
                    fn = self._download_image(marvel_data.images[0])
                    issue.image = f"{self.get_upload_image_path}{fn.name}"
                    issue.save()
                    self._upload_image(fn)
                    fn.unlink()

                self.stdout.write(self.style.SUCCESS(f"Added {issue} to database.\n\n"))
            else:
                self.stdout.write(self.style.WARNING(f"{issue} already exists...\n\n"))
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(
                    f"{series_obj} #{fnp.issue} already existing in the database.\n\n"
                )
            )

    def handle(self, *args, **options):
        m = marvelous.api(MARVEL_PUBLIC_KEY, MARVEL_PRIVATE_KEY)

        pulls = sorted(
            m.comics(
                {
                    "format": "comic",
                    "formatType": "comic",
                    "noVariants": True,
                    "dateDescriptor": "nextMonth",
                    "limit": 100,
                }
            ),
            key=lambda comic: comic.title,
        )

        fnp = FileNameParser()
        for comic in pulls:
            fnp.parse_filename(comic.title)
            self.stdout.write(f"Searching database for {fnp.series}")
            results = Series.objects.filter(
                name__icontains=fnp.series, year_began=int(fnp.year)
            )
            if results:
                correct_series = select_series_choice(results)
                if correct_series:
                    self.add_issue_to_database(correct_series, fnp, comic)
                else:
                    self.stdout.write(
                        self.style.NOTICE(
                            f"Not adding {fnp.series} #{fnp.issue} to database.\n\n"
                        )
                    )
            else:
                self.stdout.write(f"No series in database for {fnp.series}\n\n")
