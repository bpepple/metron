from django.db.models import Prefetch
from django.http import Http404
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.throttling import UserRateThrottle

from comicsdb.models import (
    Arc,
    Character,
    Creator,
    Credits,
    Issue,
    Publisher,
    Series,
    Team,
)
from comicsdb.serializers import (
    ArcSerializer,
    ArcListSerializer,
    CharacterSerializer,
    CharacterListSerializer,
    CreatorSerializer,
    CreatorListSerializer,
    IssueSerializer,
    IssueListSerializer,
    PublisherSerializer,
    PublisherListSerializer,
    SeriesSerializer,
    SeriesListSerializer,
    TeamSerializer,
    TeamListSerializer,
)


class IssueViewSetFilter(filters.FilterSet):
    series_name = filters.CharFilter(field_name="series__name", lookup_expr="icontains")
    cover_year = filters.NumberFilter(field_name="cover_date", lookup_expr="year")

    class Meta:
        model = Issue
        fields = ["series_name", "number", "cover_year"]


class ArcViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Returns a list of all the story arcs.
    retrieve:
    Returns the information of an individual story arc.
    """

    queryset = Arc.objects.all()
    filterset_fields = ("name",)
    throttle_classes = (UserRateThrottle,)

    def get_serializer_class(self):
        if self.action == "list":
            return ArcListSerializer
        if self.action == "retrieve":
            return ArcSerializer
        return ArcListSerializer

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
            serializer = IssueListSerializer(
                page, many=True, context={"request": request}
            )
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
    filterset_fields = ("name",)
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
    filterset_fields = ("name",)
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
    Return a list of all the creators.
    retrieve:
    Returns the information of an individual creator.
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
    filterset_class = IssueViewSetFilter
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
    filterset_fields = ("name",)
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
            serializer = SeriesListSerializer(
                page, many=True, context={"request": request}
            )
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
    filterset_fields = ("name", "year_began")
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
            serializer = IssueListSerializer(
                page, many=True, context={"request": request}
            )
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
    filterset_fields = ("name",)
    throttle_classes = (UserRateThrottle,)

    def get_serializer_class(self):
        if self.action == "list":
            return TeamListSerializer
        if self.action == "retrieve":
            return TeamSerializer
        return TeamListSerializer
