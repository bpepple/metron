from functools import reduce
import operator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from comicsdb.forms.series import SeriesForm
from comicsdb.models import Series, Issue


PAGINATE = 28


class SeriesList(ListView):
    model = Series
    paginate_by = PAGINATE
    queryset = (
        Series.objects
        .prefetch_related('issue_set')
    )


class SeriesIssueList(ListView):
    template_name = 'comicsdb/issue_list.html'
    paginate_by = PAGINATE

    def get_queryset(self):
        self.series = get_object_or_404(Series, slug=self.kwargs['slug'])
        return Issue.objects.select_related('series').filter(series=self.series)


class SeriesDetail(DetailView):
    model = Series
    queryset = (
        Series.objects
        .select_related('publisher')
        .prefetch_related('issue_set')
    )

    def get_context_data(self, **kwargs):
        context = super(SeriesDetail, self).get_context_data(**kwargs)
        series = self.get_object()
        try:
            next_series = (
                Series.objects
                .order_by('name')
                .filter(name__gt=series.name)
                .first()
            )
        except:
            next_series = None

        try:
            previous_series = (
                Series.objects
                .order_by('name')
                .filter(name__lt=series.name)
                .last()
            )
        except:
            previous_series = None

        context['navigation'] = {
            'next_series': next_series,
            'previous_series': previous_series,
        }
        return context


class SearchSeriesList(SeriesList):

    def get_queryset(self):
        result = super(SearchSeriesList, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)))

        return result


class SeriesCreate(LoginRequiredMixin, CreateView):
    model = Series
    form_class = SeriesForm


class SeriesUpdate(LoginRequiredMixin, UpdateView):
    model = Series
    form_class = SeriesForm


class SeriesDelete(LoginRequiredMixin, DeleteView):
    model = Series
    template_name = 'comicsdb/confirm_delete.html'
    success_url = reverse_lazy('series:list', kwargs={'page': 1})
