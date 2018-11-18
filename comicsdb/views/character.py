from functools import reduce
import operator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from comicsdb.forms.character import CharacterForm
from comicsdb.models import Character


PAGINATE = 28


class CharacterList(ListView):
    model = Character
    paginate_by = PAGINATE


class CharacterDetail(DetailView):
    model = Character

    def get_context_data(self, **kwargs):
        context = super(CharacterDetail, self).get_context_data(**kwargs)
        character = self.get_object()
        try:
            next_character = (
                Character.objects
                .filter(name__gt=character.name)
                .order_by('name').first()
            )
        except:
            next_character = None

        try:
            previous_character = (
                Character.objects
                .filter(name__lt=character.name)
                .order_by('name').last()
            )
        except:
            previous_character = None

        context['navigation'] = {
            'next_character': next_character,
            'previous_character': previous_character,
        }
        return context


class SearchCharacterList(CharacterList):

    def get_queryset(self):
        result = super(SearchCharacterList, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) | Q(alias__icontains=q) for q in query_list)))

        return result


class CharacterCreate(LoginRequiredMixin, CreateView):
    model = Character
    form_class = CharacterForm
    template_name = 'comicsdb/model_with_image_form.html'


class CharacterUpdate(LoginRequiredMixin, UpdateView):
    model = Character
    form_class = CharacterForm
    template_name = 'comicsdb/model_with_image_form.html'


class CharacterDelete(LoginRequiredMixin, DeleteView):
    model = Character
    template_name = 'comicsdb/confirm_delete.html'
    success_url = reverse_lazy('character:list', kwargs={'page': 1})
