from functools import reduce
import operator

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, Prefetch
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from comicsdb.forms.arc import ArcForm
from comicsdb.models import Arc, Issue


PAGINATE = 28


class ArcList(ListView):
    model = Arc
    paginate_by = PAGINATE


class ArcDetail(DetailView):
    model = Arc
    queryset = (
        Arc.objects
        .select_related('edited_by')
        .prefetch_related(Prefetch('issue_set',
                                   queryset=Issue.objects
                                   .order_by('cover_date', 'series__sort_name', 'number')
                                   .select_related('series')
                                   )
                          )
    )

    def get_context_data(self, **kwargs):
        context = super(ArcDetail, self).get_context_data(**kwargs)
        arc = self.get_object()
        try:
            next_arc = (
                Arc.objects
                .order_by('name')
                .filter(name__gt=arc.name)
                .first()
            )
        except:
            next_arc = None

        try:
            previous_arc = (
                Arc.objects
                .order_by('name')
                .filter(name__lt=arc.name)
                .last()
            )
        except:
            previous_arc = None

        context['navigation'] = {
            'next_arc': next_arc,
            'previous_arc': previous_arc,
        }
        return context


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

    def form_valid(self, form):
        form.instance.edited_by = self.request.user
        return super().form_valid(form)


class ArcUpdate(LoginRequiredMixin, UpdateView):
    model = Arc
    form_class = ArcForm
    template_name = 'comicsdb/model_with_image_form.html'

    def form_valid(self, form):
        form.instance.edited_by = self.request.user
        return super().form_valid(form)


class ArcDelete(PermissionRequiredMixin, DeleteView):
    model = Arc
    template_name = 'comicsdb/confirm_delete.html'
    permission_required = 'comicsdb.delete_arc'
    success_url = reverse_lazy('arc:list')
