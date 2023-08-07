from typing import Any

from django.core.management.base import BaseCommand

from comicsdb.models.issue import Issue


class Command(BaseCommand):
    help = "Print Comic Vine ID statistics."

    def handle(self, *args: Any, **options: Any) -> str | None:
        issues = Issue.objects.all()
        total = issues.count()
        missing = issues.filter(cv_id__isnull=True).count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Missing CV ID: {missing}\nWith CV ID: {total-missing}\nTotal Issues: {total}"
            )
        )
