from datetime import datetime

from django.db.models import Count
from django.db.models.functions import TruncDate, TruncMonth
from django.views.generic.base import TemplateView

from comicsdb.models import Character, Creator, Issue, Publisher


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

        # Dates used for issue counts querysets
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
        monthly_issue_dict = {}
        for issue in issues:
            month_str = issue["month"].strftime("%b")
            monthly_issue_dict.update({month_str: issue["c"]})

        # Daily Issues Added Queryset.
        # To get the last 30 items we need to reverse sort by the 'created_on' date, which
        # necessitates using python's reversed() function before creating the dict.
        res = (
            Issue.objects.annotate(day=TruncDate("created_on"))
            .values("day")
            .annotate(c=Count("day"))
            .order_by("-day")[:30]
        )
        issues = reversed(res)
        daily_issue_dict = {}
        for issue in issues:
            day_str = issue["day"].strftime("%m/%d")
            daily_issue_dict.update({day_str: issue["c"]})

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
            month_str = creator["month"].strftime("%b")
            creator_dict.update({month_str: creator["c"]})

        # Monthly Characters Added
        characters = (
            Character.objects.filter(created_on__year__gte=last_year)
            .annotate(month=TruncMonth("created_on"))
            .values("month")
            .annotate(c=Count("month"))
            .order_by("month")
        )
        character_dict = {}
        for character in characters:
            month_str = character["month"].strftime("%b")
            character_dict.update({month_str: character["c"]})

        # Assign the context values
        context["publisher_counts"] = publisher_dict
        context["monthly_issue_count"] = monthly_issue_dict
        context["daily_issue_count"] = daily_issue_dict
        context["monthly_creator"] = creator_dict
        context["monthly_character"] = character_dict

        return context
