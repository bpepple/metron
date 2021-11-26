from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from sorl.thumbnail.admin.current import AdminImageMixin

from comicsdb.models import Publisher


@admin.register(Publisher)
class PublisherAdmin(AdminImageMixin, SimpleHistoryAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "series_count")
    readonly_fields = ("modified",)
    fields = (
        "name",
        "slug",
        "modified",
        "founded",
        "desc",
        "wikipedia",
        "image",
        "edited_by",
    )
