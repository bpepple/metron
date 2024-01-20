import logging
import operator
from functools import reduce

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from comicsdb.forms.attribution import AttributionFormSet
from comicsdb.forms.universe import UniverseForm
from comicsdb.models import Attribution, Universe

PAGINATE = 28
LOGGER = logging.getLogger(__name__)


class UniverseList(ListView):
    model = Universe
    paginate_by = PAGINATE


class UniverseDetail(DetailView):
    model = Universe
    queryset = Universe.objects.select_related("edited_by")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        universe = self.get_object()
        try:
            next_universe = (
                Universe.objects.order_by("name").filter(name__gt=universe.name).first()
            )
        except ObjectDoesNotExist:
            next_universe = None

        try:
            previous_universe = (
                Universe.objects.order_by("name").filter(name__lt=universe.name).last()
            )
        except ObjectDoesNotExist:
            previous_universe = None

        context["navigation"] = {
            "next_universe": next_universe,
            "previous_universe": previous_universe,
        }
        return context


class SearchUniverseList(UniverseList):
    def get_queryset(self):
        result = super().get_queryset()
        if query := self.request.GET.get("q"):
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_, (Q(name__icontains=q) for q in query_list))
            )

        return result


class UniverseCreate(LoginRequiredMixin, CreateView):
    model = Universe
    form_class = UniverseForm
    template_name = "comicsdb/model_with_attribution_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Universe"
        if self.request.POST:
            context["attribution"] = AttributionFormSet(self.request.POST)
        else:
            context["attribution"] = AttributionFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        attribution_form = context["attribution"]
        with transaction.atomic():
            form.instance.edited_by = self.request.user
            if attribution_form.is_valid():
                self.object = form.save()
                attribution_form.instance = self.object
                attribution_form.save()
            else:
                return super().form_invalid(form)

            LOGGER.info(f"Universe: {form.instance.name} was created by {self.request.user}")
        return super().form_valid(form)


class UniverseUpdate(LoginRequiredMixin, UpdateView):
    model = Universe
    form_class = UniverseForm
    template_name = "comicsdb/model_with_attribution_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Edit information for {context['universe']}"
        if self.request.POST:
            context["attribution"] = AttributionFormSet(
                self.request.POST,
                instance=self.object,
                queryset=(Attribution.objects.filter(universes=self.object)),
                prefix="attribution",
            )
            context["attribution"].full_clean()
        else:
            context["attribution"] = AttributionFormSet(
                instance=self.object,
                queryset=(Attribution.objects.filter(universes=self.object)),
                prefix="attribution",
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        attribution_form = context["attribution"]
        with transaction.atomic():
            form.instance.edited_by = self.request.user
            if attribution_form.is_valid():
                self.object = form.save(commit=False)
                attribution_form.instance = self.object
                attribution_form.save()
            else:
                return super().form_invalid(form)

            LOGGER.info(f"Universe: {form.instance.name} was updated by {self.request.user}")
        return super().form_valid(form)


class UniverseDelete(PermissionRequiredMixin, DeleteView):
    model = Universe
    template_name = "comicsdb/confirm_delete.html"
    permission_required = "comicsdb.delete_universe"
    success_url = reverse_lazy("universe:list")
