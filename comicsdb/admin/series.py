from django.contrib import admin

from comicsdb.forms.series import SeriesForm
from comicsdb.models import Series, SeriesType


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    form = SeriesForm
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
