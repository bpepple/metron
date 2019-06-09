import operator
from functools import reduce

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from comicsdb.forms.series import SeriesForm
from comicsdb.models import Issue, Series

PAGINATE = 28


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
        qs = Series.objects.all().order_by("name", "year_began")

        # Determine if there is more than 1 series with the same name
        series_count = qs.filter(name__gte=series.name).count()

        # If there is more than one series with the same name
        # let's attempt to get the next and previous items
        if series_count > 1:
            try:
                next_series = qs.filter(
                    name=series.name, year_began__gt=series.year_began
                ).first()
            except:
                next_series = None

            try:
                previous_series = qs.filter(
                    name=series.name, year_began__lt=series.year_began
                ).last()
            except:
                previous_series = None

        if not next_series:
            try:
                next_series = qs.filter(name__gt=series.name).first()
            except:
                next_series = None

        if not previous_series:
            try:
                previous_series = qs.filter(name__lt=series.name).last()
            except:
                previous_series = None

        context["navigation"] = {
            "next_series": next_series,
            "previous_series": previous_series,
        }
        return context


class SearchSeriesList(SeriesList):
    def get_queryset(self):
        result = super(SearchSeriesList, self).get_queryset()
        query = self.request.GET.get("q")
        if query:
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
        return super().form_valid(form)


class SeriesUpdate(LoginRequiredMixin, UpdateView):
    model = Series
    form_class = SeriesForm

    def form_valid(self, form):
        form.instance.edited_by = self.request.user
        return super().form_valid(form)


class SeriesDelete(PermissionRequiredMixin, DeleteView):
    model = Series
    template_name = "comicsdb/confirm_delete.html"
    permission_required = "comicsdb.delete_series"
    success_url = reverse_lazy("series:list")
