from functools import reduce
import operator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from comicsdb.forms.series import SeriesForm
from comicsdb.models import Series


PAGINATE = 30


class SeriesList(ListView):
    model = Series
    paginate_by = PAGINATE
    queryset = (
        Series.objects
        .prefetch_related('issue_set')
    )

    def get_context_data(self, **kwargs):
        context = super(SeriesList, self).get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        return context


class SeriesDetail(DetailView):
    model = Series
    queryset = (
        Series.objects
        .select_related('publisher')
        .prefetch_related('issue_set')
    )


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
