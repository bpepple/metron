from functools import reduce
import operator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from comicsdb.forms.team import TeamForm
from comicsdb.models import Team, Issue


PAGINATE = 28


class TeamList(ListView):
    model = Team
    paginate_by = PAGINATE

    def get_context_data(self, **kwargs):
        context = super(TeamList, self).get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        return context


class TeamDetail(DetailView):
    model = Team
    queryset = (
        Team.objects
        .prefetch_related('creators', 'character_set', 'issue_set')
    )

    def get_context_data(self, **kwargs):
        context = super(TeamDetail, self).get_context_data(**kwargs)
        team = self.get_object()
        try:
            next_team = (
                Team.objects
                .filter(name__gt=team.name)
                .order_by('name').first()
            )
        except:
            next_team = None

        try:
            previous_team = (
                Team.objects
                .filter(name__lt=team.name)
                .order_by('name').last()
            )
        except:
            previous_team = None

        context['navigation'] = {
            'next_team': next_team,
            'previous_team': previous_team,
        }
        return context


class SearchTeamList(TeamList):

    def get_queryset(self):
        result = super(SearchTeamList, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)))

        return result


class TeamCreate(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'comicsdb/model_with_image_form.html'


class TeamUpdate(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'comicsdb/model_with_image_form.html'


class TeamDelete(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = 'comicsdb/confirm_delete.html'
    success_url = reverse_lazy('team:list', kwargs={'page': 1})
