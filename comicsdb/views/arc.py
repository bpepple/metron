from functools import reduce
import operator

from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from comicsdb.forms.arc import ArcForm
from comicsdb.models import Arc


PAGINATE = 30


class ArcList(ListView):
    model = Arc
    paginate_by = PAGINATE


class ArcDetail(DetailView):
    model = Arc


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


class ArcCreate(CreateView):
    model = Arc
    form_class = ArcForm


class ArcUpdate(UpdateView):
    model = Arc
    form_class = ArcForm


class ArcDelete(DeleteView):
    model = Arc
    template_name = 'comicsdb/confirm_delete.html'
    success_url = reverse_lazy('arc:list', kwargs={'page': 1})
