from dal import autocomplete
from django.forms import (
    ClearableFileInput,
    DateInput,
    ModelChoiceField,
    ModelForm,
    NumberInput,
    Select,
    Textarea,
    TextInput,
    ValidationError,
)
from django_select2 import forms as s2forms

from comicsdb.forms.team import TeamsWidget
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
            "reprints",
            "image",
        )
        widgets = {
            "series": Select(),
            "name": TextInput(attrs={"class": "input"}),
            "title": TextInput(attrs={"class": "input"}),
            "number": TextInput(attrs={"class": "input"}),
            "arcs": ArcsWidget(attrs={"class": "input"}),
            "characters": CharactersWidget(attrs={"class": "input"}),
            "teams": TeamsWidget(attrs={"class": "input"}),
            "cover_date": DateInput(
                attrs={"class": "input", "type": "date"},
            ),
            "store_date": DateInput(
                attrs={"class": "input", "type": "date"},
            ),
            "price": NumberInput(attrs={"class": "input"}),
            "isbn": TextInput(attrs={"class": "input"}),
            "sku": TextInput(attrs={"class": "input"}),
            "upc": TextInput(attrs={"class": "input"}),
            "page": TextInput(attrs={"class": "input"}),
            "cv_id": TextInput(attrs={"class": "input"}),
            "desc": Textarea(attrs={"class": "textarea"}),
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
        series: Series = self.cleaned_data["series"]
        collection_title = self.cleaned_data["title"]
        if series.series_type.id not in self.collections and collection_title:
            raise ValidationError("Collection Title field is only used for Trade Paperbacks.")
        return collection_title

    def clean_arcs(self):
        series: Series = self.cleaned_data["series"]
        arcs = self.cleaned_data["arcs"]
        if series.series_type.id in self.collections and arcs:
            raise ValidationError("Arcs cannot be added to Trade Paperbacks.")
        return arcs
