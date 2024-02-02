from dal import autocomplete
from django.forms import (
    ClearableFileInput,
    ModelChoiceField,
    ModelForm,
    ValidationError,
)
from django_select2 import forms as s2forms

from comicsdb.forms.team import TeamsWidget
from comicsdb.forms.universe import UniversesWidget
from comicsdb.models import Issue, Rating, Series


class ArcsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
    ]


class CharactersWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = ["name__icontains", "alias__icontains"]


class IssuesWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = ["series__name__icontains", "number"]


class IssueForm(ModelForm):
    series = ModelChoiceField(
        queryset=Series.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="issue:series-autocomplete",
            attrs={
                "data-placeholder": "Autocomplete...",
                "data-minimum-input-length": 3,
            },
        ),
    )

    rating = ModelChoiceField(queryset=Rating.objects.all(), empty_label=None)

    class Meta:
        model = Issue
        # exclude 'creators' field
        fields = (
            "series",
            "number",
            "title",
            "name",
            "cover_date",
            "store_date",
            "rating",
            "price",
            "sku",
            "isbn",
            "upc",
            "page",
            "cv_id",
            "desc",
            "characters",
            "teams",
            "arcs",
            "universes",
            "reprints",
            "image",
        )
        widgets = {
            "arcs": ArcsWidget(attrs={"class": "input"}),
            "characters": CharactersWidget(attrs={"class": "input"}),
            "teams": TeamsWidget(attrs={"class": "input"}),
            "universes": UniversesWidget(attrs={"class": "input"}),
            "reprints": IssuesWidget(attrs={"class": "input"}),
            "image": ClearableFileInput(),
        }
        help_texts = {
            "name": "Separate multiple story titles by a semicolon",
            "title": "Only used with Collected Editions like a Trade Paperback.",
            "price": "In United States currency",
            "reprints": (
                "Add any issues that are reprinted. Do not add a '#' "
                "in front of any issue number."
            ),
        }
        labels = {
            "name": "Story Title",
            "title": "Collection Title",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].delimiter = ";"
        self.collections = [8, 10]

    def clean_title(self):
        collection_title = self.cleaned_data["title"]
        if collection_title:
            series: Series = self.cleaned_data["series"]
            if collection_title and not series.collection:
                raise ValidationError("Collection Title field is not allowed for this series..")
        return collection_title

    def clean_arcs(self):
        arcs = self.cleaned_data["arcs"]
        if arcs:
            series: Series = self.cleaned_data["series"]
            if series.series_type.id in self.collections and arcs:
                raise ValidationError("Arcs cannot be added to Trade Paperbacks.")
        return arcs
