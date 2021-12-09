from django.db.models import Prefetch
from django.http import Http404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.throttling import UserRateThrottle

from comicsdb.filters.issue import IssueFilter
from comicsdb.filters.name import NameFilter
from comicsdb.filters.series import SeriesFilter
from comicsdb.models import Arc, Character, Creator, Credits, Issue, Publisher, Series, Team
from comicsdb.permission import IsEditor, IsEditorOrContributor
from comicsdb.serializers import (
    ArcListSerializer,
    ArcSerializer,
    CharacterListSerializer,
    CharacterSerializer,
    CreatorListSerializer,
    CreatorSerializer,
    IssueListSerializer,
    IssueSerializer,
    PublisherListSerializer,
    PublisherSerializer,
    SeriesListSerializer,
    SeriesSerializer,
    TeamListSerializer,
    TeamSerializer,
)


class ArcViewSet(viewsets.ModelViewSet):
    """
    list:
    Returns a list of all the story arcs.

    retrieve:
    Returns the information of an individual story arc.
    """

    queryset = Arc.objects.all()
    filterset_class = NameFilter
    throttle_classes = (UserRateThrottle,)

    def get_serializer_class(self):
        if self.action == "list":
            return ArcListSerializer
        return ArcSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsEditor]
        elif self.action in ["retrieve", "list"]:
            permission_classes = [IsEditorOrContributor]
        return [permission() for permission in permission_classes]

    @action(detail=True)
    def issue_list(self, request, pk=None):
        """
        Returns a list of issues for a story arc.
        """
        arc = self.get_object()
        queryset = arc.issue_set.select_related("series").order_by(
            "cover_date", "series", "number"
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = IssueListSerializer(page, many=True, context={"request": request})
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
    filterset_class = NameFilter
    throttle_classes = (UserRateThrottle,)

    def get_serializer_class(self):
        if self.action == "list":
            return CharacterListSerializer
        if self.action == "retrieve":
            return CharacterSerializer
        return CharacterListSerializer


class CreatorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of all the creators.

    retrieve:
    Returns the information of an individual creator.
    """

    queryset = Creator.objects.all()
    filterset_class = NameFilter
    throttle_classes = (UserRateThrottle,)

    def get_serializer_class(self):
        if self.action == "list":
            return CreatorListSerializer
        if self.action == "retrieve":
            return CreatorSerializer
        return CreatorListSerializer


class IssueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of all the issues.

    retrieve:
    Returns the information of an individual issue.
    """

    queryset = Issue.objects.select_related("series").prefetch_related(
        Prefetch(
            "credits_set",
            queryset=Credits.objects.order_by("creator__name")
            .distinct("creator__name")
            .select_related("creator")
            .prefetch_related("role"),
        )
    )
    filterset_class = IssueFilter
    throttle_classes = (UserRateThrottle,)

    def get_serializer_class(self):
        if self.action == "list":
            return IssueListSerializer
        if self.action == "retrieve":
            return IssueSerializer
        return IssueListSerializer


class PublisherViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Returns a list of all publishers.

    retrieve:
    Returns the information of an individual publisher.
    """

    queryset = Publisher.objects.prefetch_related("series_set")
    filterset_class = NameFilter
    throttle_classes = (UserRateThrottle,)

    def get_serializer_class(self):
        if self.action == "list":
            return PublisherListSerializer
        if self.action == "retrieve":
            return PublisherSerializer
        return PublisherListSerializer

    @action(detail=True)
    def series_list(self, request, pk=None):
        """
        Returns a list of series for a publisher.
        """
        publisher = self.get_object()
        queryset = publisher.series_set.select_related("series_type").prefetch_related(
            "issue_set"
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SeriesListSerializer(page, many=True, context={"request": request})
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

    queryset = Series.objects.select_related("series_type", "publisher")
    serializer_class = SeriesSerializer
    filterset_class = SeriesFilter
    throttle_classes = (UserRateThrottle,)

    def get_serializer_class(self):
        if self.action == "list":
            return SeriesListSerializer
        if self.action == "retrieve":
            return SeriesSerializer
        return SeriesListSerializer

    @action(detail=True)
    def issue_list(self, request, pk=None):
        """
        Returns a list of issues for a series.
        """
        series = self.get_object()
        queryset = series.issue_set.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = IssueListSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        else:
            raise Http404()


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of all the teams.

    retrieve:
    Returns the information of an individual team.
    """

    queryset = Team.objects.all()
    filterset_class = NameFilter
    throttle_classes = (UserRateThrottle,)

    def get_serializer_class(self):
        if self.action == "list":
            return TeamListSerializer
        if self.action == "retrieve":
            return TeamSerializer
        return TeamListSerializer
