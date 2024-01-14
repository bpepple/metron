from datetime import datetime

from chartkick.django import ColumnChart, PieChart
from django.db.models import Count
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from comicsdb.models import Arc, Character, Creator, Issue, Publisher, Series, Team


def create_pub_dict() -> dict[str, int]:
    publishers = Publisher.objects.annotate(num_issues=Count("series__issue")).values(
        "name", "num_issues"
    )
    return {publisher["name"]: publisher["num_issues"] for publisher in publishers}


def create_monthly_issue_dict() -> dict[str, int]:
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

    return monthly_issue_dict


def create_daily_issue_dict() -> dict[str, int]:
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
    return daily_issue_dict


def create_creator_dict() -> dict[str, int]:
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
    return creator_dict


def create_character_dict() -> dict[str, int]:
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
    return character_dict


def create_year_count_dict():
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
    return year_count_dict


@cache_page(timeout=60 * 30)  # Cache for 30 minutes
def statistics(request):
    # Resource totals
    update_time = datetime.now()
    publishers_total = Publisher.objects.count()
    series_total = Series.objects.count()
    issues_total = Issue.objects.count()
    characters_total = Character.objects.count()
    creators_total = Creator.objects.count()
    teams_total = Team.objects.count()
    arcs_total = Arc.objects.count()

    # Time based statistics
    pub_chart = PieChart(
        create_pub_dict(),
        title="Percentage of Issues by Publisher",
        thousands=",",
        legend=False,
    )
    year_chart = PieChart(
        create_year_count_dict(), title="Number of Issues Added per Year", thousands=","
    )
    daily_chart = ColumnChart(
        create_daily_issue_dict(), title="Number of Issues for the last 30 days"
    )
    monthly_chart = ColumnChart(
        create_monthly_issue_dict(), title="Number of Issues Added by Month", thousands=","
    )
    creator_chart = ColumnChart(
        create_creator_dict(), title="Number of Creators Added by Month"
    )
    character_chart = ColumnChart(
        create_character_dict(),
        title="Number of Characters Added by Month",
    )

    return render(
        request,
        "comicsdb/statistics.html",
        {
            "publisher_count": pub_chart,
            "year_count": year_chart,
            "daily_chart": daily_chart,
            "monthly_chart": monthly_chart,
            "creator_chart": creator_chart,
            "character_chart": character_chart,
            "publishers_total": publishers_total,
            "series_total": series_total,
            "issues_total": issues_total,
            "characters_total": characters_total,
            "creators_total": creators_total,
            "teams_total": teams_total,
            "arcs_total": arcs_total,
            "update_time": update_time,
        },
    )
