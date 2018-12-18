from functools import reduce
import operator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q, Prefetch
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from comicsdb.forms.credits import CreditsFormSet
from comicsdb.forms.issue import IssueForm
from comicsdb.models import Issue, Credits


PAGINATE = 28


class IssueList(ListView):
    model = Issue
    paginate_by = PAGINATE
    queryset = (
        Issue.objects
        .select_related('series')
    )


class IssueDetail(DetailView):
    model = Issue
    queryset = (
        Issue.objects
        .select_related('series')
        .prefetch_related(Prefetch('credits_set',
                                   queryset=Credits.objects
                                   .order_by('creator__name')
                                   .distinct('creator__name')
                                   .select_related('creator')
                                   .prefetch_related('role')))
    )

    def get_context_data(self, **kwargs):
        context = super(IssueDetail, self).get_context_data(**kwargs)
        issue = self.get_object()
        try:
            next_issue = issue.get_next_by_cover_date(series=issue.series)
        except ObjectDoesNotExist:
            next_issue = None

        try:
            previous_issue = issue.get_previous_by_cover_date(
                series=issue.series)
        except ObjectDoesNotExist:
            previous_issue = None

        context['navigation'] = {
            'next_issue': next_issue,
            'previous_issue': previous_issue,
        }
        return context


class SearchIssueList(IssueList):

    # Currently only searching the Series Name but down the road
    # I'll look at implementing a better search engine.
    def get_queryset(self):
        result = super(SearchIssueList, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(series__name__icontains=q) | Q(number__in=q) for q in query_list)))

        return result


class IssueCreate(LoginRequiredMixin, CreateView):
    model = Issue
    form_class = IssueForm

    def get_context_data(self, **kwargs):
        data = super(IssueCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['credits'] = CreditsFormSet(self.request.POST)
        else:
            data['credits'] = CreditsFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        credits_form = context['credits']
        with transaction.atomic():
            self.object = form.save()

            if credits_form.is_valid():
                credits_form.instance = self.object
                credits_form.save()
        return super(IssueCreate, self).form_valid(form)


class IssueUpdate(LoginRequiredMixin, UpdateView):
    model = Issue
    form_class = IssueForm

    def get_context_data(self, **kwargs):
        data = super(IssueUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['credits'] = CreditsFormSet(self.request.POST,
                                             instance=self.object)
        else:
            data['credits'] = CreditsFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        credits_form = context['credits']
        with transaction.atomic():
            self.object = form.save()

            if credits_form.is_valid():
                credits_form.instance = self.object
                credits_form.save()
        return super(IssueUpdate, self).form_valid(form)


class IssueDelete(LoginRequiredMixin, DeleteView):
    model = Issue
    template_name = 'comicsdb/confirm_delete.html'
    success_url = reverse_lazy('issue:list')
