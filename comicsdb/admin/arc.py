from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from sorl.thumbnail.admin.current import AdminImageMixin

from comicsdb.models import Arc


@admin.register(Arc)
class ArcAdmin(AdminImageMixin, SimpleHistoryAdmin):
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    field = ("name", "slug", "desc", "image")
