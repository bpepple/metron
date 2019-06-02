from datetime import date, datetime

from django.views.generic import ListView

from comicsdb.models import Issue


PAGINATE = 28

current_week = date.today().isocalendar()[1]
current_year = date.today().year
# The '3' in the format string gives the date for Wednesday
release_day = datetime.strptime(f'{current_year}-{current_week}-3', '%G-%V-%u')


class WeekList(ListView):
    model = Issue
    paginate_by = PAGINATE
    template_name = 'comicsdb/week_list.html'
    queryset = (
        Issue.objects
        .filter(store_date__week=current_week)
        .filter(store_date__year=current_year)
        .prefetch_related('series')
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['release_day'] = release_day
        return context
