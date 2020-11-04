import logging

from comicsdb.filters.issue import IssueFilter
from comicsdb.forms.credits import CreditsFormSet
from comicsdb.forms.issue import IssueForm
from comicsdb.models import Creator, Credits, Issue, Series
from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Prefetch, Q
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

PAGINATE = 28
LOGGER = logging.getLogger(__name__)


class SeriesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Series.objects.none()

        qs = Series.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class CreatorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Creator.objects.none()

        qs = Creator.objects.all()

        if self.q:
            qs = qs.filter(
                # Unaccent lookup won't work on alias array field.
                Q(first_name__unaccent__icontains=self.q)
                | Q(last_name__unaccent__icontains=self.q)
                | Q(alias__icontains=self.q)
            )

        return qs


class IssueList(ListView):
    model = Issue
    paginate_by = PAGINATE
    queryset = Issue.objects.select_related("series")


class IssueDetail(DetailView):
    model = Issue
    queryset = Issue.objects.select_related(
        "series", "series__publisher"
    ).prefetch_related(
        Prefetch(
            "credits_set",
            queryset=Credits.objects.order_by(
                "creator__last_name", "creator__first_name"
            )
            .distinct("creator__last_name", "creator__first_name")
            .select_related("creator")
            .prefetch_related("role"),
        )
    )

    def get_context_data(self, **kwargs):
        context = super(IssueDetail, self).get_context_data(**kwargs)
        issue = self.get_object()
        try:
            next_issue = issue.get_next_by_cover_date(series=issue.series)
        except ObjectDoesNotExist:
            next_issue = None

        try:
            previous_issue = issue.get_previous_by_cover_date(series=issue.series)
        except ObjectDoesNotExist:
            previous_issue = None

        context["navigation"] = {
            "next_issue": next_issue,
            "previous_issue": previous_issue,
        }
        return context


class SearchIssueList(IssueList):
    def get_queryset(self):
        result = super(SearchIssueList, self).get_queryset()
        issue_result = IssueFilter(self.request.GET, queryset=result)

        return issue_result.qs


class IssueCreate(LoginRequiredMixin, CreateView):
    model = Issue
    form_class = IssueForm

    def get_context_data(self, **kwargs):
        data = super(IssueCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data["credits"] = CreditsFormSet(self.request.POST)
        else:
            data["credits"] = CreditsFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        credits_form = context["credits"]
        with transaction.atomic():
            form.instance.edited_by = self.request.user
            self.object = form.save()

            if credits_form.is_valid():
                credits_form.instance = self.object
                credits_form.save()

            LOGGER.info(
                f"Issue: {form.instance.series} #{form.instance.number} was created by {self.request.user}"
            )
        return super(IssueCreate, self).form_valid(form)


class IssueUpdate(LoginRequiredMixin, UpdateView):
    model = Issue
    form_class = IssueForm

    def get_context_data(self, **kwargs):
        data = super(IssueUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data["credits"] = CreditsFormSet(
                self.request.POST,
                instance=self.object,
                queryset=(
                    Credits.objects.filter(issue=self.object).prefetch_related("role")
                ),
            )
        else:
            data["credits"] = CreditsFormSet(
                instance=self.object,
                queryset=(
                    Credits.objects.filter(issue=self.object).prefetch_related("role")
                ),
            )
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        credits_form = context["credits"]
        with transaction.atomic():
            form.instance.edited_by = self.request.user
            self.object = form.save()

            if credits_form.is_valid():
                credits_form.instance = self.object
                credits_form.save()

            LOGGER.info(
                f"Issue: {form.instance.series} #{form.instance.number} was updated by {self.request.user}"
            )
        return super(IssueUpdate, self).form_valid(form)


class IssueDelete(PermissionRequiredMixin, DeleteView):
    model = Issue
    template_name = "comicsdb/confirm_delete.html"
    permission_required = "comicsdb.delete_issue"
    success_url = reverse_lazy("issue:list")
