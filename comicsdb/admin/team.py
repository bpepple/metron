from django.contrib import admin
from sorl.thumbnail.admin.current import AdminImageMixin

from comicsdb.models import Team


@admin.register(Team)
class TeamAdmin(AdminImageMixin, admin.ModelAdmin):
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    # form view
    fieldsets = (
        (None, {"fields": ("name", "slug", "desc", "wikipedia", "image", "edited_by")}),
        ("Related", {"fields": ("creators",)}),
    )
    filter_horizontal = ("creators",)
