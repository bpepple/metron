from functools import reduce
import operator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from comicsdb.forms.arc import ArcForm
from comicsdb.models import Arc, Issue


PAGINATE = 30


class ArcList(ListView):
    model = Arc
    paginate_by = PAGINATE


class ArcDetail(DetailView):
    model = Arc
    queryset = (
        Arc.objects
        .prefetch_related(Prefetch('issue_set',
                                   queryset=Issue.objects.order_by('cover_date', 'series', 'number')),
                          'issue_set__series')
    )


class SearchArcList(ArcList):

    def get_queryset(self):
        result = super(SearchArcList, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)))

        return result


class ArcCreate(LoginRequiredMixin, CreateView):
    model = Arc
    form_class = ArcForm
    template_name = 'comicsdb/model_with_image_form.html'


class ArcUpdate(LoginRequiredMixin, UpdateView):
    model = Arc
    form_class = ArcForm
    template_name = 'comicsdb/model_with_image_form.html'


class ArcDelete(LoginRequiredMixin, DeleteView):
    model = Arc
    template_name = 'comicsdb/confirm_delete.html'
    success_url = reverse_lazy('arc:list', kwargs={'page': 1})
