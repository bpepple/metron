from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from comicsdb.models import (
    Arc,
    Character,
    Credits,
    Creator,
    Issue,
    Publisher,
    Role,
    Series,
    SeriesType,
    Team,
    Variant,
)

from comicsdb.forms.issue import IssueForm
from comicsdb.forms.credits import CreditsForm


class CreditsInline(admin.TabularInline):
    model = Credits
    form = CreditsForm
    extra = 1


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1


@admin.register(Arc)
class ArcAdmin(AdminImageMixin, admin.ModelAdmin):
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    field = ("name", "slug", "desc", "image")


@admin.register(Character)
class CharacterAdmin(AdminImageMixin, admin.ModelAdmin):
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    # form view
    fieldsets = (
        (None, {"fields": ("name", "slug", "desc", "wikipedia", "alias", "image")}),
        ("Related", {"fields": ("creators", "teams")}),
    )
    filter_horizontal = ("creators", "teams")


@admin.register(Creator)
class CreatorAdmin(AdminImageMixin, admin.ModelAdmin):
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("modified",)
    field = ("name", "slug", "modified", "birth", "death", "desc", "wikipedia", "image")


@admin.register(Issue)
class IssueAdmin(AdminImageMixin, admin.ModelAdmin):
    form = IssueForm
    search_fields = ("series__name",)
    list_display = ("__str__",)
    list_filter = ("cover_date", "store_date", "series__publisher")
    list_select_related = ("series",)
    date_hierarchy = "cover_date"
    # form view
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "series",
                    "number",
                    "name",
                    "cover_date",
                    "store_date",
                    "slug",
                    "desc",
                    "image",
                )
            },
        ),
        ("Related", {"fields": ("characters", "teams", "arcs")}),
    )
    filter_horizontal = ("arcs", "characters", "teams")
    inlines = (CreditsInline, VariantInline)


@admin.register(Publisher)
class PublisherAdmin(AdminImageMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "series_count")
    readonly_fields = ("modified",)
    fields = ("name", "slug", "modified", "founded", "desc", "wikipedia", "image")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    readonly_fields = ("modified",)
    fields = ("name", "notes", "order", "modified")


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "year_began")
    list_filter = ("publisher",)
    prepopulated_fields = {"slug": ("name", "year_began")}
    fields = (
        "name",
        "slug",
        "sort_name",
        "publisher",
        "volume",
        "year_began",
        "year_end",
        "series_type",
        "desc",
    )


@admin.register(SeriesType)
class SeriesTypeAdmin(admin.ModelAdmin):
    fields = ("name", "notes")


@admin.register(Team)
class TeamAdmin(AdminImageMixin, admin.ModelAdmin):
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    # form view
    fieldsets = (
        (None, {"fields": ("name", "slug", "desc", "wikipedia", "image")}),
        ("Related", {"fields": ("creators",)}),
    )
    filter_horizontal = ("creators",)
