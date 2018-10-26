from django.views.generic import ListView, DetailView

from comicsdb.models import Publisher


PAGINATE = 30


class PublisherList(ListView):
    model = Publisher
    paginate_by = PAGINATE


class PublisherDetail(DetailView):
    model = Publisher
