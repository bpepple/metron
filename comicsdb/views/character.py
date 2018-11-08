from functools import reduce
import operator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from comicsdb.forms.character import CharacterForm
from comicsdb.models import Character


PAGINATE = 30


class CharacterList(ListView):
    model = Character
    paginate_by = PAGINATE


class CharacterDetail(DetailView):
    model = Character
    queryset = (
        Character.objects
        .prefetch_related('issue_set')
    )


class SearchCharacterList(CharacterList):

    def get_queryset(self):
        result = super(SearchCharacterList, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(last_name__icontains=q) for q in query_list)))

        return result


class CharacterCreate(LoginRequiredMixin, CreateView):
    model = Character
    form_class = CharacterForm


class CharacterUpdate(LoginRequiredMixin, UpdateView):
    model = Character
    form_class = CharacterForm


class CharacterDelete(LoginRequiredMixin, DeleteView):
    model = Character
    template_name = 'comicsdb/confirm_delete.html'
    success_url = reverse_lazy('character:list', kwargs={'page': 1})
