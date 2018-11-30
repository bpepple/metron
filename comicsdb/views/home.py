from django.views.generic import TemplateView

from comicsdb.models import (Publisher, Series, Issue, Character,
                             Creator, Team, Arc)


class HomePageView(TemplateView):
    template_name = 'comicsdb/home.html'

#     TODO: Need to implement a better solution in the future
#           but for now this should be fine.
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['publisher'] = Publisher.objects.all().count()
        context['series'] = Series.objects.all().count()
        context['issue'] = Issue.objects.all().count()
        context['character'] = Character.objects.all().count()
        context['creator'] = Creator.objects.all().count()
        context['team'] = Team.objects.all().count()
        context['arc'] = Arc.objects.all().count()

        return context
