from functools import reduce
import operator

from django.db.models import Q
from django.views.generic import ListView, DetailView

from comicsdb.models import Publisher


PAGINATE = 30


class PublisherList(ListView):
    model = Publisher
    paginate_by = PAGINATE


class PublisherDetail(DetailView):
    model = Publisher


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
