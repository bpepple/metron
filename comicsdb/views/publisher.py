from functools import reduce
import operator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from comicsdb.forms.publisher import PublisherForm
from comicsdb.models import Publisher, Series
from django.shortcuts import get_object_or_404


PAGINATE = 28


class PublisherList(ListView):
    model = Publisher
    paginate_by = PAGINATE


class PublisherSeriesList(ListView):
    template_name = 'comicsdb/series_list.html'
    paginate_by = PAGINATE

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, slug=self.kwargs['slug'])
        return Series.objects.filter(publisher=self.publisher)


class PublisherDetail(DetailView):
    model = Publisher
    queryset = (
        Publisher.objects
        .prefetch_related('series_set')
    )

    def get_context_data(self, **kwargs):
        context = super(PublisherDetail, self).get_context_data(**kwargs)
        publisher = self.get_object()
        try:
            next_publisher = (
                Publisher.objects
                .order_by('name')
                .filter(name__gt=publisher.name)
                .first()
            )
        except:
            next_publisher = None

        try:
            previous_publisher = (
                Publisher.objects
                .order_by('name')
                .filter(name__lt=publisher.name)
                .last()
            )
        except:
            previous_publisher = None

        context['navigation'] = {
            'next_publisher': next_publisher,
            'previous_publisher': previous_publisher,
        }
        return context


class SearchPublisherList(PublisherList):

    def get_queryset(self):
        result = super(SearchPublisherList, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)))

        return result


class PublisherCreate(LoginRequiredMixin, CreateView):
    model = Publisher
    form_class = PublisherForm
    template_name = 'comicsdb/model_with_image_form.html'


class PublisherUpdate(LoginRequiredMixin, UpdateView):
    model = Publisher
    form_class = PublisherForm
    template_name = 'comicsdb/model_with_image_form.html'


class PublisherDelete(LoginRequiredMixin, DeleteView):
    model = Publisher
    template_name = 'comicsdb/confirm_delete.html'
    success_url = reverse_lazy('publisher:list')
