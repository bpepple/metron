from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import (
    ClearableFileInput,
    DateInput,
    ModelForm,
    Select,
    Textarea,
    TextInput,
)

from comicsdb.models import Issue


class IssueForm(ModelForm):
    class Media:
        css = {"all": ("admin/css/widgets.css",)}
        js = (("/jsi18n"),)

    class Meta:
        model = Issue
        # exclude 'creators' field
        fields = (
            "series",
            "number",
            "slug",
            "name",
            "cover_date",
            "store_date",
            "desc",
            "characters",
            "teams",
            "arcs",
            "image",
        )
        widgets = {
            "series": Select(),
            "name": TextInput(attrs={"class": "input"}),
            "slug": TextInput(attrs={"class": "input"}),
            "number": TextInput(attrs={"class": "input"}),
            "arcs": FilteredSelectMultiple(
                "Story Arcs", attrs={"size": "6"}, is_stacked=False
            ),
            "characters": FilteredSelectMultiple(
                "Characters", attrs={"size": "6"}, is_stacked=False
            ),
            "teams": FilteredSelectMultiple(
                "Teams", attrs={"size": "6"}, is_stacked=False
            ),
            "cover_date": DateInput(attrs={"class": "input", "type": "date"},),
            "store_date": DateInput(attrs={"class": "input", "type": "date"},),
            "desc": Textarea(attrs={"class": "textarea"}),
            "image": ClearableFileInput(),
        }
        help_texts = {"name": "Separate multiple story titles by a semicolon"}
        labels = {"name": "Story Title"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].delimiter = ";"
