from django.http import Http404
from rest_framework import viewsets, filters
from rest_framework.decorators import action

from comicsdb.models import Publisher, Series
from comicsdb.serializers import PublisherSerializer, SeriesSerializer, IssueSerializer


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

    @action(detail=True)
    def series_list(self, request, pk=None):
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


class SeriesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Returns a list of all the comic series.
    retrieve:
    Returns the information of an individual comic series.
    """
    queryset = (
        Series.objects
        .prefetch_related('issue_set')
    )
    serializer_class = SeriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @action(detail=True)
    def issue_list(self, request, pk=None):
        """
        Returns a list of issues for a series.
        """
        series = self.get_object()
        queryset = (
            series.issue_set
            .prefetch_related('credits_set', 'credits_set__creator', 'credits_set__role', 'arcs', 'characters')
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = IssueSerializer(
                page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        else:
            raise Http404()
