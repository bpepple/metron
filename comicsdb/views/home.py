from datetime import date

from django.views.generic import TemplateView

from comicsdb.models import (Publisher, Series, Issue, Character,
                             Creator, Team, Arc)


class HomePageView(TemplateView):
    template_name = 'comicsdb/home.html'

    def get_context_data(self, **kwargs):
        current_week = date.today().isocalendar()[1]
        last_week = current_week - 1
        current_year = date.today().year

        context = super(HomePageView, self).get_context_data(**kwargs)
        context['publisher'] = Publisher.objects.count()
        context['series'] = Series.objects.count()
        context['issue'] = Issue.objects.count()
        context['character'] = Character.objects.count()
        context['creator'] = Creator.objects.count()
        context['team'] = Team.objects.count()
        context['arc'] = Arc.objects.count()
        context['recent'] = (
            Issue.objects
            .prefetch_related('series')
            .order_by('-modified')
            .all()[:10]
        )
        context['current_week'] = (
            Issue.objects
            .filter(store_date__week=current_week)
            .filter(store_date__year=current_year)
            .prefetch_related('series')
        )
        context['last_week'] = (
            Issue.objects
            .filter(store_date__week=last_week)
            .filter(store_date__year=current_year)
            .prefetch_related('series')
        )
        context

        return context
