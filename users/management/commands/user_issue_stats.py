from django.core.management.base import BaseCommand
from users.models import CustomUser
from django.db.models import Count


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        if qs := CustomUser.objects.annotate(num_issues=Count("issue__created_by")).order_by(
            "-num_issues"
        ):
            title_str = "Issues added count by user:"
            underline_title = "".join("-" for _ in range(len(title_str)))
            print(f"{title_str}\n{underline_title}")
            for q in qs:
                if q.num_issues > 0:
                    print(f"{q}: {q.num_issues}")
        else:
            print("No issues have been added.")
