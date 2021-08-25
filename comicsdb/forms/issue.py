from dal import autocomplete
from django.contrib.admin.widgets import FilteredSelectMultiple
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

from comicsdb.models import Issue, Series


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
            "desc",
            "characters",
            "teams",
            "arcs",
            "image",
        )
        widgets = {
            "series": Select(),
            "name": TextInput(attrs={"class": "input"}),
            "number": TextInput(attrs={"class": "input"}),
            "arcs": FilteredSelectMultiple(
                "Story Arcs", attrs={"size": "6"}, is_stacked=False
            ),
            "characters": FilteredSelectMultiple(
                "Characters", attrs={"size": "6"}, is_stacked=False
            ),
            "teams": FilteredSelectMultiple("Teams", attrs={"size": "6"}, is_stacked=False),
            "cover_date": DateInput(
                attrs={"class": "input", "type": "date"},
            ),
            "store_date": DateInput(
                attrs={"class": "input", "type": "date"},
            ),
            "price": NumberInput(attrs={"class": "input"}),
            "sku": TextInput(attrs={"class": "input"}),
            "upc": TextInput(attrs={"class": "input"}),
            "desc": Textarea(attrs={"class": "textarea"}),
            "image": ClearableFileInput(),
        }
        help_texts = {
            "name": "Separate multiple story titles by a semicolon",
            "price": "In United States currency",
        }
        labels = {"name": "Story Title"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].delimiter = ";"
