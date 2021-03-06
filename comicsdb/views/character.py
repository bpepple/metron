import logging
import operator
from functools import reduce

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Prefetch, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from comicsdb.forms.character import CharacterForm
from comicsdb.models import Character, Issue, Series

PAGINATE = 28
LOGGER = logging.getLogger(__name__)


class CharacterSeriesList(ListView):
    paginate_by = PAGINATE
    template_name = "comicsdb/issue_list.html"

    def get_queryset(self):
        self.series = get_object_or_404(Series, slug=self.kwargs["series"])
        self.character = get_object_or_404(Character, slug=self.kwargs["character"])

        return Issue.objects.select_related("series").filter(
            characters=self.character, series=self.series
        )


class CharacterList(ListView):
    model = Character
    paginate_by = PAGINATE
    queryset = Character.objects.prefetch_related("issue_set")


class CharacterIssueList(ListView):
    paginate_by = PAGINATE
    template_name = "comicsdb/issue_list.html"

    def get_queryset(self):
        self.character = get_object_or_404(Character, slug=self.kwargs["slug"])
        return Issue.objects.select_related("series").filter(characters=self.character)

    def get_context_data(self, **kwargs):
        context = super(CharacterIssueList, self).get_context_data(**kwargs)
        context["title"] = self.character
        return context


class CharacterDetail(DetailView):
    model = Character
    queryset = Character.objects.select_related("edited_by").prefetch_related(
        Prefetch(
            "issue_set",
            queryset=Issue.objects.order_by(
                "series__sort_name", "cover_date", "number"
            ).select_related("series"),
        )
    )

    def get_context_data(self, **kwargs):
        context = super(CharacterDetail, self).get_context_data(**kwargs)
        character = self.get_object()
        qs = Character.objects.order_by("name")
        try:
            next_character = qs.filter(name__gt=character.name).first()
        except ObjectDoesNotExist:
            next_character = None

        try:
            previous_character = qs.filter(name__lt=character.name).last()
        except ObjectDoesNotExist:
            previous_character = None

        # TODO: Look into improving this queryset
        #
        # Run this context queryset if the issue count is greater than 0.
        if character.issue_count:
            series_issues = (
                Character.objects.filter(id=character.id)
                .values(
                    "issue__series__name",
                    "issue__series__year_began",
                    "issue__series__slug",
                )
                .annotate(Count("issue"))
                .order_by("issue__series__sort_name", "issue__series__year_began")
            )
            context["appearances"] = series_issues
        else:
            context["appearances"] = ""

        context["navigation"] = {
            "next_character": next_character,
            "previous_character": previous_character,
        }
        return context


class SearchCharacterList(CharacterList):
    def get_queryset(self):
        result = super(SearchCharacterList, self).get_queryset()
        query = self.request.GET.get("q")
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(
                    operator.and_,
                    (Q(name__icontains=q) | Q(alias__icontains=q) for q in query_list),
                )
            )

        return result


class CharacterCreate(LoginRequiredMixin, CreateView):
    model = Character
    form_class = CharacterForm
    template_name = "comicsdb/model_with_image_form.html"

    def get_context_data(self, **kwargs):
        context = super(CharacterCreate, self).get_context_data(**kwargs)
        context["title"] = "Add Character"
        return context

    def form_valid(self, form):
        form.instance.edited_by = self.request.user
        LOGGER.info(
            f"Character: {form.instance.name} was created by {self.request.user}"
        )
        return super().form_valid(form)


class CharacterUpdate(LoginRequiredMixin, UpdateView):
    model = Character
    form_class = CharacterForm
    template_name = "comicsdb/model_with_image_form.html"

    def get_context_data(self, **kwargs):
        context = super(CharacterUpdate, self).get_context_data(**kwargs)
        context["title"] = f"Edit information for {context['character']}"
        return context

    def form_valid(self, form):
        form.instance.edited_by = self.request.user
        LOGGER.info(
            f"Character: {form.instance.name} was updated by {self.request.user}"
        )
        return super().form_valid(form)


class CharacterDelete(PermissionRequiredMixin, DeleteView):
    model = Character
    template_name = "comicsdb/confirm_delete.html"
    permission_required = "comicsdb.delete_character"
    success_url = reverse_lazy("character:list")
