from django.db.models import Prefetch
from django.http import Http404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.throttling import UserRateThrottle

from comicsdb.filters.issue import IssueFilter
from comicsdb.filters.name import NameFilter
from comicsdb.filters.series import SeriesFilter
from comicsdb.models import (
    Arc,
    Character,
    Creator,
    Credits,
    Issue,
    Publisher,
    Role,
    Series,
    Team,
)
from comicsdb.models.series import SeriesType
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
    RoleSerializer,
    SeriesListSerializer,
    SeriesSerializer,
    SeriesTypeSerializer,
    TeamListSerializer,
    TeamSerializer,
)


class ArcViewSet(viewsets.ReadOnlyModelViewSet):
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
        match self.action:
            case "retrieve":
                return ArcSerializer
            case _:
                return ArcListSerializer

    @action(detail=True)
    def issue_list(self, request, pk=None):
        """
        Returns a list of issues for a story arc.
        """
        arc = self.get_object()
        queryset = arc.issue_set.select_related("series", "series__series_type").order_by(
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
        match self.action:
            case "retrieve":
                return CharacterSerializer
            case _:
                return CharacterListSerializer

    @action(detail=True)
    def issue_list(self, request, pk=None):
        """
        Returns a list of issues for a character.
        """
        character = self.get_object()
        queryset = character.issue_set.select_related(
            "series", "series__series_type"
        ).order_by("cover_date", "series", "number")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = IssueListSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        else:
            raise Http404()


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
        match self.action:
            case "retrieve":
                return CreatorSerializer
            case _:
                return CreatorListSerializer


class IssueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of all the issues.

    retrieve:
    Returns the information of an individual issue.
    """

    queryset = Issue.objects.select_related("series", "series__series_type").prefetch_related(
        Prefetch(
            "credits_set",
            queryset=Credits.objects.order_by("creator__name")
            .distinct("creator__name")
            .select_related("creator")
            .prefetch_related("role"),
        ),
        Prefetch(
            "reprints",
            queryset=Issue.objects.select_related("series", "series__series_type"),
        ),
    )
    filterset_class = IssueFilter
    throttle_classes = (UserRateThrottle,)

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return IssueSerializer
            case _:
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
        match self.action:
            case "retrieve":
                return PublisherSerializer
            case _:
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


class RoleViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
    Returns a list of all the creator roles.
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filterset_class = NameFilter
    throttle_classes = (UserRateThrottle,)


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
        match self.action:
            case "retrieve":
                return SeriesSerializer
            case _:
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


class SeriesTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
    Returns a list of the Series Types available.
    """

    queryset = SeriesType.objects.all()
    serializer_class = SeriesTypeSerializer
    filterset_class = NameFilter
    throttle_classes = (UserRateThrottle,)


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
        match self.action:
            case "retrieve":
                return TeamSerializer
            case _:
                return TeamListSerializer

    @action(detail=True)
    def issue_list(self, request, pk=None):
        """
        Returns a list of issues for a character.
        """
        team = self.get_object()
        queryset = team.issue_set.select_related("series", "series__series_type").order_by(
            "cover_date", "series", "number"
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = IssueListSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        else:
            raise Http404()
