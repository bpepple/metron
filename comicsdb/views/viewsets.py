from django.http import Http404
from rest_framework import viewsets, filters
from rest_framework.decorators import action

from comicsdb.models import Arc, Character, Publisher, Series
from comicsdb.serializers import (ArcSerializer, CharacterSerializer, CharacterListSerializer,
                                  IssueSerializer, PublisherSerializer, SeriesSerializer)


class ArcViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Returns a list of all the story arcs.
    retrieve:
    Returns the information of an individual story arc.
    """
    queryset = Arc.objects.all()
    serializer_class = ArcSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @action(detail=True)
    def issue_list(self, request, pk=None):
        """
        Returns a list of issues for a story arc.
        """
        arc = self.get_object()
        queryset = (
            arc.issue_set
            .select_related('series')
            .prefetch_related('credits_set', 'credits_set__creator',
                              'credits_set__role', 'characters', 'arcs')
            .order_by('cover_date', 'series', 'number')
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = IssueSerializer(
                page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        else:
            raise Http404()


class CharacterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of all the characters.
    retrieve:
    Returns the information of an individual character.
    """
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'alias')

    def get_serializer_class(self):
        if self.action == 'list':
            return CharacterListSerializer
        if self.action == 'retrieve':
            return CharacterSerializer
        return CharacterListSerializer


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
