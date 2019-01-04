from functools import reduce
import operator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from comicsdb.forms.creator import CreatorForm
from comicsdb.models import Creator, Credits


PAGINATE = 28


class CreatorList(ListView):
    model = Creator
    paginate_by = PAGINATE


class CreatorDetail(DetailView):
    model = Creator
    queryset = (
        Creator.objects
        .prefetch_related(Prefetch('credits_set',
                                   queryset=Credits.objects
                                   .order_by('issue__cover_date', 'issue__series', 'issue__number')
                                   .select_related('issue', 'issue__series'))
                          )
    )

    def get_context_data(self, **kwargs):
        context = super(CreatorDetail, self).get_context_data(**kwargs)
        creator = self.get_object()
        try:
            next_creator = (
                Creator.objects
                .order_by('name')
                .filter(name__gt=creator.name)
                .first()
            )
        except:
            next_creator = None

        try:
            previous_creator = (
                Creator.objects
                .order_by('name')
                .filter(name__lt=creator.name)
                .last()
            )
        except:
            previous_creator = None

        context['navigation'] = {
            'next_creator': next_creator,
            'previous_creator': previous_creator,
        }
        return context


class SearchCreatorList(CreatorList):

    def get_queryset(self):
        result = super(SearchCreatorList, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__unaccent__icontains=q) for q in query_list)))

        return result


class CreatorCreate(LoginRequiredMixin, CreateView):
    model = Creator
    form_class = CreatorForm
    template_name = 'comicsdb/model_with_image_form.html'


class CreatorUpdate(LoginRequiredMixin, UpdateView):
    model = Creator
    form_class = CreatorForm
    template_name = 'comicsdb/model_with_image_form.html'


class CreatorDelete(LoginRequiredMixin, DeleteView):
    model = Creator
    template_name = 'comicsdb/confirm_delete.html'
    success_url = reverse_lazy('creator:list')
