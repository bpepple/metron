from django.contrib import admin
from sorl.thumbnail.admin.current import AdminImageMixin

from comicsdb.admin.util import AttributionInline
from comicsdb.models import Team


@admin.register(Team)
class TeamAdmin(AdminImageMixin, admin.ModelAdmin):
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("created_on", "modified")
    autocomplete_fields = ["creators", "universes"]
    # form view
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "desc",
                    "creators",
                    "universes",
                    "image",
                    "edited_by",
                )
            },
        ),
    )
    inlines = [AttributionInline]
