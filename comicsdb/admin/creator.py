from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from sorl.thumbnail.admin.current import AdminImageMixin

from comicsdb.models import Creator


@admin.register(Creator)
class CreatorAdmin(AdminImageMixin, SimpleHistoryAdmin):
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("modified",)
    field = ("name", "slug", "modified", "birth", "death", "desc", "wikipedia", "image")
