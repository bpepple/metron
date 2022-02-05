import logging
import operator
from functools import reduce

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from comicsdb.forms.series import SeriesForm
from comicsdb.models import Issue, Series

PAGINATE = 28
LOGGER = logging.getLogger(__name__)


class SeriesList(ListView):
    model = Series
    paginate_by = PAGINATE
    queryset = Series.objects.prefetch_related("issue_set")


class SeriesIssueList(ListView):
    template_name = "comicsdb/issue_list.html"
    paginate_by = PAGINATE

    def get_queryset(self):
        self.series = get_object_or_404(Series, slug=self.kwargs["slug"])
        return Issue.objects.select_related("series").filter(series=self.series)

    def get_context_data(self, **kwargs):
        context = super(SeriesIssueList, self).get_context_data(**kwargs)
        context["title"] = self.series
        return context


class SeriesDetail(DetailView):
    model = Series
    queryset = Series.objects.select_related("publisher", "edited_by").prefetch_related(
        "issue_set"
    )

    def get_context_data(self, **kwargs):
        context = super(SeriesDetail, self).get_context_data(**kwargs)
        series = self.get_object()

        # Set the initial value for the navigation variables
        next_series = None
        previous_series = None

        # Create the base queryset with all the series.
        qs = Series.objects.all().order_by("sort_name", "year_began")

        # Determine if there is more than 1 series with the same name
        series_count = qs.filter(sort_name__gte=series.sort_name).count()

        # If there is more than one series with the same name
        # let's attempt to get the next and previous items
        if series_count > 1:
            try:
                next_series = qs.filter(
                    sort_name=series.sort_name, year_began__gt=series.year_began
                ).first()
            except ObjectDoesNotExist:
                next_series = None

            try:
                previous_series = qs.filter(
                    sort_name=series.sort_name, year_began__lt=series.year_began
                ).last()
            except ObjectDoesNotExist:
                previous_series = None

        if not next_series:
            try:
                next_series = qs.filter(sort_name__gt=series.sort_name).first()
            except ObjectDoesNotExist:
                next_series = None

        if not previous_series:
            try:
                previous_series = qs.filter(sort_name__lt=series.sort_name).last()
            except ObjectDoesNotExist:
                previous_series = None

        # Top 10 creator credits for series. Might be worthwhile to exclude editors, etc.
        creators = (
            series.issue_set.values("creators__name", "creators__image", "creators__slug")
            .order_by("creators")
            .annotate(count=Count("creators"))
            .order_by("-count", "creators__name")
            .filter(count__gte=1)[:12]
        )

        # Top 10 character appearances for series.
        characters = (
            series.issue_set.values(
                "characters__name", "characters__image", "characters__slug"
            )
            .order_by("characters")
            .annotate(count=Count("characters"))
            .order_by("-count", "characters__name")
            .filter(count__gte=1)[:12]
        )

        context["navigation"] = {
            "next_series": next_series,
            "previous_series": previous_series,
        }
        context["creators"] = creators
        context["characters"] = characters
        return context


class SearchSeriesList(SeriesList):
    def get_queryset(self):
        result = super(SearchSeriesList, self).get_queryset()
        if query := self.request.GET.get("q"):
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_, (Q(name__icontains=q) for q in query_list))
            )

        return result


class SeriesCreate(LoginRequiredMixin, CreateView):
    model = Series
    form_class = SeriesForm

    def form_valid(self, form):
        form.instance.edited_by = self.request.user
        LOGGER.info(f"Series: {form.instance.name} was created by {self.request.user}")
        return super().form_valid(form)


class SeriesUpdate(LoginRequiredMixin, UpdateView):
    model = Series
    form_class = SeriesForm

    def form_valid(self, form):
        form.instance.edited_by = self.request.user
        LOGGER.info(f"Series: {form.instance.name} was updated by {self.request.user}")
        return super().form_valid(form)


class SeriesDelete(PermissionRequiredMixin, DeleteView):
    model = Series
    template_name = "comicsdb/confirm_delete.html"
    permission_required = "comicsdb.delete_series"
    success_url = reverse_lazy("series:list")
