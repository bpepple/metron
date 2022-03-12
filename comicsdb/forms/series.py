from django.forms import ModelForm, Select, Textarea, TextInput
from django_select2 import forms as s2forms

from comicsdb.models import Series


class SeriesWidget(s2forms.ModelSelect2Widget):
    search_fields = ["name__icontains"]


class MultiSeriesWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = ["name__icontains"]


class SeriesForm(ModelForm):
    class Meta:
        model = Series
        exclude = ("edited_by", "slug")
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "sort_name": TextInput(attrs={"class": "input"}),
            "volume": TextInput(attrs={"class": "input"}),
            "year_began": TextInput(attrs={"class": "input"}),
            "year_end": TextInput(attrs={"class": "input"}),
            "type": Select(),
            "publisher": Select(),
            "desc": Textarea(attrs={"class": "textarea"}),
            "associated": MultiSeriesWidget(attrs={"class": "input"}),
        }
        help_texts = {
            "sort_name": """Most of the time it will be the same as the series name,
            but if the title starts with an article like 'The' it might be remove so
            that it is listed with like named series.""",
            "year_end": "Leave blank if a One-Shot, Annual, or Ongoing Series.",
            "associated": "Associate the series with another series. For example, an annual with it's primary series.",
        }
        labels = {"associated": "Associated Series"}

    field_order = [
        "name",
        "sort_name",
        "volume",
        "year_began",
        "year_end",
        "type",
        "publisher",
        "desc",
        "associated",
    ]
