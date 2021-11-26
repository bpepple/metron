from django.contrib import admin
from django.forms.models import ModelForm
from django.forms.widgets import Select, Textarea, TextInput
from searchableselect.widgets import SearchableSelect
from simple_history.admin import SimpleHistoryAdmin

from comicsdb.models import Series, SeriesType


class SeriesAdminForm(ModelForm):
    class Meta:
        model = Series
        exclude = ()
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "sort_name": TextInput(attrs={"class": "input"}),
            "volume": TextInput(attrs={"class": "input"}),
            "year_began": TextInput(attrs={"class": "input"}),
            "year_end": TextInput(attrs={"class": "input"}),
            "series_type": Select(),
            "associated": SearchableSelect(
                model="comicsdb.Series", search_field="name", many=True, limit=200
            ),
            "publisher": Select(),
            "desc": Textarea(attrs={"class": "textarea"}),
        }
        help_texts = {
            "sort_name": """Most of the time it will be the same as the series name,
            but if the title starts with an article like 'The' it might be remove so
            that it is listed with like named series.""",
            "year_end": "Leave blank if a One-Shot, Annual, or Ongoing Series.",
            "associated": "Associate a series with another. For example an annual with it's primary series.",
        }
        labels = {"associated": "Associated Series"}


@admin.register(Series)
class SeriesAdmin(SimpleHistoryAdmin):
    form = SeriesAdminForm
    search_fields = ("name",)
    list_display = ("name", "year_began")
    list_filter = ("modified", "publisher")
    prepopulated_fields = {"slug": ("name", "year_began")}
    fields = (
        "name",
        "slug",
        "sort_name",
        "publisher",
        "volume",
        "year_began",
        "year_end",
        "series_type",
        "associated",
        "desc",
        "edited_by",
    )


@admin.register(SeriesType)
class SeriesTypeAdmin(admin.ModelAdmin):
    fields = ("name", "notes")
