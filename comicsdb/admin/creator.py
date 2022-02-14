from django.contrib import admin
from sorl.thumbnail.admin.current import AdminImageMixin

from comicsdb.admin.util import AttributionInline
from comicsdb.models import Creator


@admin.register(Creator)
class CreatorAdmin(AdminImageMixin, admin.ModelAdmin):
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("modified",)
    field = ("name", "slug", "modified", "birth", "death", "desc", "image")
    inlines = [AttributionInline]
