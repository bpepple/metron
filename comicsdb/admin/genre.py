from django.contrib import admin

from comicsdb.models.genre import Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    readonly_fields = ("modified",)
    fields = ("name", "desc", "modified")
