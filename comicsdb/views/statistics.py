from datetime import datetime
from time import strftime

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.views.generic.base import TemplateView

from comicsdb.models import Creator, Issue, Publisher


class StatisticsView(TemplateView):
    template_name = "comicsdb/statistics.html"

    def get_context_data(self, **kwargs):
        context = super(StatisticsView, self).get_context_data(**kwargs)
        # Publisher Issue Counts
        publishers = Publisher.objects.annotate(
            num_issues=Count("series__issue")
        ).values("name", "num_issues")

        publisher_dict = {}
        for publisher in publishers:
            publisher_dict.update({publisher["name"]: publisher["num_issues"]})

        # Monthly Issues Added Counts
        today = datetime.now()
        last_year = today.year - 1

        # This should show the last 24 months probably need to refine the
        # queryset to show something more reasonable like 12 months.
        issues = (
            Issue.objects.filter(created_on__year__gte=last_year)
            .annotate(month=TruncMonth("created_on"))
            .values("month")
            .annotate(c=Count("month"))
            .order_by("month")
        )
        issue_dict = {}
        for issue in issues:
            month_str = issue["month"].strftime("%b '%y")
            issue_dict.update({month_str: issue["c"]})

        # Monthly Creators Added
        creators = (
            Creator.objects.filter(created_on__year__gte=last_year)
            .annotate(month=TruncMonth("created_on"))
            .values("month")
            .annotate(c=Count("month"))
            .order_by("month")
        )
        creator_dict = {}
        for creator in creators:
            month_str = creator["month"].strftime("%b '%y")
            creator_dict.update({month_str: creator["c"]})

        # Assign the context values
        context["publisher_counts"] = publisher_dict
        context["monthly_issues"] = issue_dict
        context["monthly_creator"] = creator_dict

        return context
