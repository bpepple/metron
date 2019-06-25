from datetime import datetime
from time import strftime

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.views.generic.base import TemplateView

from comicsdb.models import Issue, Publisher


class StatisticsView(TemplateView):
    template_name = "comicsdb/statistics.html"

    def get_context_data(self, **kwargs):
        context = super(StatisticsView, self).get_context_data(**kwargs)
        # Publisher Issue Counts
        data = Publisher.objects.annotate(num_issues=Count("series__issue")).values(
            "name", "num_issues"
        )

        count_dict = {}
        for pub in data:
            count_dict.update({pub["name"]: pub["num_issues"]})

        # Monthly Issues Added Counts
        today = datetime.now()
        last_year = today.year - 1

        # This should show the last 24 months probably need to refine the
        # queryset to show something more reasonable like 12 months.
        add_issue = (
            Issue.objects.filter(created_on__year__gte=last_year)
            .annotate(month=TruncMonth("created_on"))
            .values("month")
            .annotate(c=Count("month"))
            .order_by("month")
        )
        add_dict = {}
        for i in add_issue:
            month_str = i["month"].strftime("%b '%y")
            add_dict.update({month_str: i["c"]})

        # Assign the context values
        context["pub_issues"] = count_dict
        context["monthly_add_count"] = add_dict

        return context
