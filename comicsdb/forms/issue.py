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
)
from django_select2 import forms as s2forms

from comicsdb.forms.team import TeamsWidget
from comicsdb.models import Issue, Series


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

    class Media:
        css = {"all": ("admin/css/widgets.css",)}
        js = (("/jsi18n"),)

    class Meta:
        model = Issue
        # exclude 'creators' field
        fields = (
            "series",
            "number",
            "name",
            "cover_date",
            "store_date",
            "price",
            "sku",
            "upc",
            "page",
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
            "sku": TextInput(attrs={"class": "input"}),
            "upc": TextInput(attrs={"class": "input"}),
            "page": TextInput(attrs={"class": "input"}),
            "desc": Textarea(attrs={"class": "textarea"}),
            "reprints": IssuesWidget(attrs={"class": "input"}),
            "image": ClearableFileInput(),
        }
        help_texts = {
            "name": "Separate multiple story titles by a semicolon",
            "price": "In United States currency",
            "reprints": "Add any issues that are reprinted.",
        }
        labels = {"name": "Story Title"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].delimiter = ";"
