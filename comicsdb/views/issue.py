from functools import reduce
import operator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Prefetch
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from comicsdb.forms.issue import IssueForm
from comicsdb.models import Issue, Credits


PAGINATE = 30


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
                                   queryset=Credits.objects.distinct('creator__last_name', 'creator__first_name')),
                          'credits_set__creator', 'credits_set__role')
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
                       (Q(series__name__icontains=q) for q in query_list)))

        return result


class IssueCreate(LoginRequiredMixin, CreateView):
    model = Issue
    form_class = IssueForm
    template_name = 'comicsdb/model_with_image_form.html'


class IssueUpdate(LoginRequiredMixin, UpdateView):
    model = Issue
    form_class = IssueForm
    template_name = 'comicsdb/model_with_image_form.html'


class IssueDelete(LoginRequiredMixin, DeleteView):
    model = Issue
    template_name = 'comicsdb/confirm_delete.html'
    success_url = reverse_lazy('issue:list', kwargs={'page': 1})
