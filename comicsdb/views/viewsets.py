from django.http import Http404
from rest_framework import viewsets, filters
from rest_framework.decorators import action

from comicsdb.models import Publisher
from comicsdb.serializers import PublisherSerializer, SeriesSerializer


class PublisherViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Returns a list of all publishers.
    retrieve:
    Returns the information of an individual publisher.
    """
    queryset = (
        Publisher.objects
        .prefetch_related('series_set')
    )
    serializer_class = PublisherSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    @action(detail=True)
    def series_list(self, request, slug=None):
        """
        Returns a list of series for a publisher.
        """
        publisher = self.get_object()
        queryset = (
            publisher.series_set
            .prefetch_related('issue_set')
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SeriesSerializer(page, many=True,
                                          context={"request": request})
            return self.get_paginated_response(serializer.data)
        else:
            raise Http404()
