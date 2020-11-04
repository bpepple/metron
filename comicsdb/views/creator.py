import logging
import operator
from functools import reduce

from comicsdb.forms.creator import CreatorForm
from comicsdb.models import Creator, Credits, Issue, Series
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

PAGINATE = 28
LOGGER = logging.getLogger(__name__)


class CreatorSeriesList(ListView):
    paginate_by = PAGINATE
    template_name = "comicsdb/issue_list.html"

    def get_queryset(self):
        self.series = get_object_or_404(Series, slug=self.kwargs["series"])
        self.creator = get_object_or_404(Creator, slug=self.kwargs["creator"])
        return Issue.objects.select_related("series").filter(
            creators=self.creator, series=self.series
        )


class CreatorIssueList(ListView):
    paginate_by = PAGINATE
    template_name = "comicsdb/issue_list.html"

    def get_queryset(self):
        self.creator = get_object_or_404(Creator, slug=self.kwargs["slug"])
        return Issue.objects.select_related("series").filter(creators=self.creator)

    def get_context_data(self, **kwargs):
        context = super(CreatorIssueList, self).get_context_data(**kwargs)
        context["title"] = self.creator
        return context


class CreatorList(ListView):
    model = Creator
    paginate_by = PAGINATE
    queryset = Creator.objects.prefetch_related("credits_set")


class CreatorDetail(DetailView):
    model = Creator
    queryset = Creator.objects.select_related("edited_by")

    def get_context_data(self, **kwargs):
        context = super(CreatorDetail, self).get_context_data(**kwargs)
        creator = self.get_object()
        qs = Creator.objects.order_by("last_name", "first_name")
        try:
            next_creator = qs.filter(
                last_name__gt=creator.last_name, first_name__gt=creator.first_name
            ).first()
        except ObjectDoesNotExist:
            next_creator = None

        try:
            previous_creator = qs.filter(
                last_name__lt=creator.last_name, first_name__lt=creator.first_name
            ).last()
        except ObjectDoesNotExist:
            previous_creator = None

        context["navigation"] = {
            "next_creator": next_creator,
            "previous_creator": previous_creator,
        }

        series_issues = (
            Credits.objects.filter(creator=creator)
            .values(
                "issue__series__name",
                "issue__series__year_began",
                "issue__series__slug",
            )
            .annotate(Count("issue"))
            .order_by("issue__series__sort_name", "issue__series__year_began")
        )
        context["credits"] = series_issues

        return context


class SearchCreatorList(CreatorList):
    def get_queryset(self):
        result = super(SearchCreatorList, self).get_queryset()
        query = self.request.GET.get("q")
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(
                    operator.and_,
                    (
                        # Unaccent lookup won't work on alias array field.
                        Q(first_name__unaccent__icontains=q)
                        | Q(last_name__unaccent__icontains=q)
                        | Q(alias__icontains=q)
                        for q in query_list
                    ),
                )
            )

        return result


class CreatorCreate(LoginRequiredMixin, CreateView):
    model = Creator
    form_class = CreatorForm
    template_name = "comicsdb/creator_form.html"

    def form_valid(self, form):
        form.instance.edited_by = self.request.user
        LOGGER.info(
            f"Creator: {form.instance.get_full_name} was created by {self.request.user}"
        )
        return super().form_valid(form)


class CreatorUpdate(LoginRequiredMixin, UpdateView):
    model = Creator
    form_class = CreatorForm
    template_name = "comicsdb/creator_form.html"

    def form_valid(self, form):
        form.instance.edited_by = self.request.user
        LOGGER.info(
            f"Creator: {form.instance.get_full_name} was updated by {self.request.user}"
        )
        return super().form_valid(form)


class CreatorDelete(PermissionRequiredMixin, DeleteView):
    model = Creator
    template_name = "comicsdb/confirm_delete.html"
    permission_required = "comicsdb.delete_creator"
    success_url = reverse_lazy("creator:list")
