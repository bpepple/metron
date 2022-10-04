from django.contrib import admin

from comicsdb.models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    ordering = ("id",)
    list_display = ("name", "short_description")
    search_fields = ("name",)
