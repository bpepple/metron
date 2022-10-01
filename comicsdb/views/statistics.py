from django.db.models import Count
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.views.generic.base import TemplateView

from comicsdb.models import Arc, Character, Creator, Issue, Publisher, Series, Team


class StatisticsView(TemplateView):
    template_name = "comicsdb/statistics.html"

    def get_context_data(self, **kwargs):
        context = super(StatisticsView, self).get_context_data(**kwargs)
        # Publisher Issue Counts
        publishers = Publisher.objects.annotate(num_issues=Count("series__issue")).values(
            "name", "num_issues"
        )

        publisher_dict = {
            publisher["name"]: publisher["num_issues"] for publisher in publishers
        }

        # Monthly Issues Added Queryset
        res = (
            Issue.objects.annotate(month=TruncMonth("created_on"))
            .values("month")
            .annotate(c=Count("month"))
            .order_by("-month")[:12]
        )
        monthly_issue_dict = {}
        for issue in reversed(res):
            month_str = issue["month"].strftime("%b")
            monthly_issue_dict[month_str] = issue["c"]

        # Daily Issues Added Queryset.
        # To get the last 30 items we need to reverse sort by the 'created_on' date, which
        # necessitates using python's reversed() function before creating the dict.
        res = (
            Issue.objects.annotate(day=TruncDate("created_on"))
            .values("day")
            .annotate(c=Count("day"))
            .order_by("-day")[:30]
        )
        daily_issue_dict = {}
        for issue in reversed(res):
            day_str = issue["day"].strftime("%m/%d")
            daily_issue_dict[day_str] = issue["c"]

        # Monthly Creators Added
        res = (
            Creator.objects.annotate(month=TruncMonth("created_on"))
            .values("month")
            .annotate(c=Count("month"))
            .order_by("-month")[:12]
        )
        creator_dict = {}
        for creator in reversed(res):
            month_str = creator["month"].strftime("%b")
            creator_dict[month_str] = creator["c"]

        # Monthly Characters Added
        res = (
            Character.objects.annotate(month=TruncMonth("created_on"))
            .values("month")
            .annotate(c=Count("month"))
            .order_by("-month")[:12]
        )
        character_dict = {}
        for character in reversed(res):
            month_str = character["month"].strftime("%b")
            character_dict[month_str] = character["c"]

        # Issues add by year
        res = (
            Issue.objects.annotate(year=TruncYear("created_on"))
            .values("year")
            .annotate(c=Count("year"))
            .order_by("year")
        )
        year_count_dict = {}
        for year_count in res:
            year_str = year_count["year"].strftime("%Y")
            year_count_dict[year_str] = year_count["c"]

        # Assign the context values
        context["publisher_counts"] = publisher_dict
        context["monthly_issue_count"] = monthly_issue_dict
        context["daily_issue_count"] = daily_issue_dict
        context["monthly_creator"] = creator_dict
        context["monthly_character"] = character_dict
        context["yearly_count"] = year_count_dict

        # TODO: Look into using len(publisher_dict)
        context["publishers"] = Publisher.objects.count()
        context["series"] = Series.objects.count()
        context["issues"] = Issue.objects.count()
        context["characters"] = Character.objects.count()
        context["creators"] = Creator.objects.count()
        context["teams"] = Team.objects.count()
        context["arcs"] = Arc.objects.count()

        return context
