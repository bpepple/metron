from functools import reduce
import operator

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from comicsdb.forms.team import TeamForm
from comicsdb.models import Team


PAGINATE = 28


class TeamList(ListView):
    model = Team
    paginate_by = PAGINATE


class TeamDetail(DetailView):
    model = Team
    queryset = Team.objects.select_related("edited_by")

    def get_context_data(self, **kwargs):
        context = super(TeamDetail, self).get_context_data(**kwargs)
        team = self.get_object()
        try:
            next_team = Team.objects.filter(name__gt=team.name).order_by("name").first()
        except:
            next_team = None

        try:
            previous_team = (
                Team.objects.filter(name__lt=team.name).order_by("name").last()
            )
        except:
            previous_team = None

        context["navigation"] = {"next_team": next_team, "previous_team": previous_team}
        return context


class SearchTeamList(TeamList):
    def get_queryset(self):
        result = super(SearchTeamList, self).get_queryset()
        query = self.request.GET.get("q")
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_, (Q(name__icontains=q) for q in query_list))
            )

        return result


class TeamCreate(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = "comicsdb/model_with_image_form.html"

    def form_valid(self, form):
        form.instance.edited_by = self.request.user
        return super().form_valid(form)


class TeamUpdate(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = "comicsdb/model_with_image_form.html"

    def form_valid(self, form):
        form.instance.edited_by = self.request.user
        return super().form_valid(form)


class TeamDelete(PermissionRequiredMixin, DeleteView):
    model = Team
    template_name = "comicsdb/confirm_delete.html"
    permission_required = "comicsdb.delete_team"
    success_url = reverse_lazy("team:list")
