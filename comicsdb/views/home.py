from django.views.generic import TemplateView

from comicsdb.models import (Publisher, Series, Issue, Character,
                             Creator, Team, Arc)


class HomePageView(TemplateView):
    template_name = 'comicsdb/home.html'

#     TODO: Need to implement a better solution in the future
#           but for now this should be fine.
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['publisher'] = Publisher.objects.count()
        context['series'] = Series.objects.count()
        context['issue'] = Issue.objects.count()
        context['character'] = Character.objects.count()
        context['creator'] = Creator.objects.count()
        context['team'] = Team.objects.count()
        context['arc'] = Arc.objects.count()

        return context
