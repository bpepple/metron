from datetime import date, datetime

from django.views.generic import ListView

from comicsdb.models import Issue

PAGINATE = 28


class WeekList(ListView):
    year, week, _ = date.today().isocalendar()

    model = Issue
    paginate_by = PAGINATE
    template_name = "comicsdb/week_list.html"
    queryset = (
        Issue.objects.filter(store_date__week=week)
        .filter(store_date__year=year)
        .prefetch_related("series")
    )

    def get_context_data(self, **kwargs):
        # The '3' in the format string gives the date for Wednesday
        release_day = datetime.strptime(f"{self.year}-{self.week}-3", "%G-%V-%u")
        context = super().get_context_data(**kwargs)
        context["release_day"] = release_day
        return context
