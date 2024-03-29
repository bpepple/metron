from typing import Any

from django.core.management.base import BaseCommand

from comicsdb.models.issue import Issue


class Command(BaseCommand):
    help = "Fix bad issue story data."

    def handle(self, *args: Any, **options: Any) -> str | None:
        qs = Issue.objects.filter(name=None)
        if qs.count() > 0:
            for i in qs:
                i.name = []
            fix_count = Issue.objects.bulk_update(qs, ["name"])
            self.stdout.write(self.style.SUCCESS(f"Fixed {fix_count} issues."))
        else:
            self.stdout.write(self.style.WARNING("Nothing to fix."))
