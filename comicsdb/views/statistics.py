from datetime import datetime

from chartkick.django import ColumnChart, PieChart
from django.core.cache import cache
from django.db.models import Count
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.shortcuts import render

from comicsdb.models import Arc, Character, Creator, Issue, Publisher, Series, Team

# Cache time to live is 30 minutes.
CACHE_TTL = 60 * 30


def create_pub_dict() -> dict[str, int]:
    publishers = cache.get("publishers")
    if not publishers:
        publishers = Publisher.objects.annotate(num_issues=Count("series__issue")).values(
            "name", "num_issues"
        )
        cache.set("publishers", publishers, CACHE_TTL)
    return {publisher["name"]: publisher["num_issues"] for publisher in publishers}


def create_monthly_issue_dict() -> dict[str, int]:
    monthly_issues = cache.get("monthly_issues")
    if not monthly_issues:
        monthly_issues = (
            Issue.objects.annotate(month=TruncMonth("created_on"))
            .values("month")
            .annotate(c=Count("month"))
            .order_by("-month")[:12]
        )
        cache.set("monthly_issues", monthly_issues, CACHE_TTL)
    monthly_issue_dict = {}
    for issue in reversed(monthly_issues):
        month_str = issue["month"].strftime("%b")
        monthly_issue_dict[month_str] = issue["c"]

    return monthly_issue_dict


def create_daily_issue_dict() -> dict[str, int]:
    # To get the last 30 items we need to reverse sort by the 'created_on' date, which
    # necessitates using python's reversed() function before creating the dict.
    daily_issues = cache.get("daily_issues")
    if not daily_issues:
        daily_issues = (
            Issue.objects.annotate(day=TruncDate("created_on"))
            .values("day")
            .annotate(c=Count("day"))
            .order_by("-day")[:30]
        )
        cache.set("daily_issues", daily_issues, CACHE_TTL)

    daily_issue_dict = {}
    for issue in reversed(daily_issues):
        day_str = issue["day"].strftime("%m/%d")
        daily_issue_dict[day_str] = issue["c"]
    return daily_issue_dict


def create_creator_dict() -> dict[str, int]:
    creators = cache.get("creators")
    if not creators:
        creators = (
            Creator.objects.annotate(month=TruncMonth("created_on"))
            .values("month")
            .annotate(c=Count("month"))
            .order_by("-month")[:12]
        )
        cache.set("creators", creators, CACHE_TTL)

    creator_dict = {}
    for creator in reversed(creators):
        month_str = creator["month"].strftime("%b")
        creator_dict[month_str] = creator["c"]
    return creator_dict


def create_character_dict() -> dict[str, int]:
    characters = cache.get("characters")
    if not characters:
        characters = (
            Character.objects.annotate(month=TruncMonth("created_on"))
            .values("month")
            .annotate(c=Count("month"))
            .order_by("-month")[:12]
        )
        cache.set("characters", characters, CACHE_TTL)

    character_dict = {}
    for character in reversed(characters):
        month_str = character["month"].strftime("%b")
        character_dict[month_str] = character["c"]
    return character_dict


def create_year_count_dict():
    years_count = cache.get("year_count_dict")
    if not years_count:
        years_count = (
            Issue.objects.annotate(year=TruncYear("created_on"))
            .values("year")
            .annotate(c=Count("year"))
            .order_by("year")
        )
        cache.set("year_count_dict", years_count, CACHE_TTL)

    year_count_dict = {}
    for year_count in years_count:
        year_str = year_count["year"].strftime("%Y")
        year_count_dict[year_str] = year_count["c"]
    return year_count_dict


def statistics(request):
    # Resource totals
    update_time = cache.get("stats_update_time")
    if not update_time:
        update_time = datetime.now()
        cache.set("stats_update_time", update_time, CACHE_TTL)

    publishers_total = cache.get("publishers_total")
    if not publishers_total:
        publishers_total = Publisher.objects.count()
        cache.set("publishers_total", publishers_total, CACHE_TTL)

    series_total = cache.get("series_total")
    if not series_total:
        series_total = Series.objects.count()
        cache.set("series_total", series_total, CACHE_TTL)

    issues_total = cache.get("issue_total")
    if not issues_total:
        issues_total = Issue.objects.count()
        cache.set("issue_total", issues_total, CACHE_TTL)

    characters_total = cache.get("characters_total")
    if not characters_total:
        characters_total = Character.objects.count()
        cache.set("characters_total", characters_total, CACHE_TTL)

    creators_total = cache.get("creators_total")
    if not creators_total:
        creators_total = Creator.objects.count()
        cache.set("creators_total", creators_total, CACHE_TTL)

    teams_total = cache.get("teams_total")
    if not teams_total:
        teams_total = Team.objects.count()
        cache.set("teams_total", teams_total, CACHE_TTL)

    arcs_total = cache.get("arcs_total")
    if not arcs_total:
        arcs_total = Arc.objects.count()
        cache.set("arcs_total", arcs_total, CACHE_TTL)

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
