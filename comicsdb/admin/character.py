from django.contrib import admin
from sorl.thumbnail.admin.current import AdminImageMixin

from comicsdb.admin.util import AttributionInline
from comicsdb.models import Character


@admin.register(Character)
class CharacterAdmin(AdminImageMixin, admin.ModelAdmin):
    search_fields = ("name", "alias")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("created_on", "modified")
    autocomplete_fields = ["creators", "teams"]
    # form view
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "desc",
                    "alias",
                    "creators",
                    "teams",
                    "image",
                    "edited_by",
                )
            },
        ),
    )
    inlines = [AttributionInline]
