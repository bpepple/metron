from django.contrib import admin

from comicsdb.models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["title", "start_date", "end_date", "active"]
    fields = ["title", "content", "start_date", "end_date", "display_type", "active"]
