from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm, Select, Textarea, TextInput

from comicsdb.models import Series


class SeriesForm(ModelForm):
    class Media:
        css = {"all": ("admin/css/widgets.css",)}
        js = (("/jsi18n"),)

    class Meta:
        model = Series
        exclude = ("edited_by", "slug")
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "sort_name": TextInput(attrs={"class": "input"}),
            "volume": TextInput(attrs={"class": "input"}),
            "year_began": TextInput(attrs={"class": "input"}),
            "year_end": TextInput(attrs={"class": "input"}),
            "series_type": Select(),
            "publisher": Select(),
            "desc": Textarea(attrs={"class": "textarea"}),
            "associated": FilteredSelectMultiple(
                "Associated Series", attrs={"size": "6"}, is_stacked=False
            ),
        }
        help_texts = {
            "sort_name": """Most of the time it will be the same as the series name,
            but if the title starts with an article like 'The' it might be remove so
            that it is listed with like named series.""",
            "year_end": "Leave blank if a One-Shot, Annual, or Ongoing Series.",
            "associated": "Associate a series with another. For example, an annual with it's primary series.",
        }
        labels = {"associated": "Associated Series"}

    field_order = [
        "name",
        "sort_name",
        "volume",
        "year_began",
        "year_end",
        "series_type",
        "publisher",
        "desc",
        "associated",
    ]
