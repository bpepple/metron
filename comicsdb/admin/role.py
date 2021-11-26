from django.contrib import admin

from comicsdb.models import Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    readonly_fields = ("modified",)
    fields = ("name", "notes", "order", "modified")
