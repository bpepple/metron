from functools import reduce
import operator

from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from comicsdb.forms.creator import CreatorForm
from comicsdb.models import Creator


PAGINATE = 30


class CreatorList(ListView):
    model = Creator
    paginate_by = PAGINATE


class CreatorDetail(DetailView):
    model = Creator


class SearchCreatorList(CreatorList):

    def get_queryset(self):
        result = super(SearchCreatorList, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)))

        return result


class CreatorCreate(CreateView):
    model = Creator
    form_class = CreatorForm


class CreatorUpdate(UpdateView):
    model = Creator
    form_class = CreatorForm


class CreatorDelete(DeleteView):
    model = Creator
    template_name = 'comicsdb/confirm_delete.html'
    success_url = reverse_lazy('creator:list', kwargs={'page': 1})
