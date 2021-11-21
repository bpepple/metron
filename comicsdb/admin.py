import datetime
from typing import Any, Optional

from django.contrib import admin
from django.db.models.query import QuerySet
from django.forms.models import ModelForm
from django.forms.widgets import Select, Textarea, TextInput
from searchableselect.widgets import SearchableSelect
from simple_history.admin import SimpleHistoryAdmin
from sorl.thumbnail.admin import AdminImageMixin

from comicsdb.forms.credits import CreditsForm
from comicsdb.forms.issue import IssueForm
from comicsdb.models import (
    Arc,
    Character,
    Creator,
    Credits,
    Issue,
    Publisher,
    Role,
    Series,
    SeriesType,
    Team,
    Variant,
)


class FutureStoreDateListFilter(admin.SimpleListFilter):
    title = "future store week"

    parameter_name = "store_date"

    def lookups(self, request: Any, model_admin: Any):
        return (("thisWeek", "This week"), ("nextWeek", "Next week"))

    def queryset(self, request: Any, queryset: QuerySet) -> Optional[QuerySet]:
        today = datetime.date.today()
        year, week, _ = today.isocalendar()

        if self.value() == "thisWeek":
            return queryset.filter(store_date__week=week, store_date__year=year)

        if self.value() == "nextWeek":
            return queryset.filter(store_date__week=week + 1, store_date__year=year)


class CreditsInline(admin.TabularInline):
    model = Credits
    form = CreditsForm
    extra = 1


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1


def add_dc_credits(modeladmin, request, queryset):
    jim = Creator.objects.get(slug="jim-lee")
    marie = Creator.objects.get(slug="marie-javins")
    eic = Role.objects.get(name__iexact="editor in chief")
    pub = Role.objects.get(name__iexact="publisher")
    chief = Role.objects.get(name__iexact="Chief Creative Officer")
    for i in queryset:
        jc, create = Credits.objects.get_or_create(issue=i, creator=jim)
        if create:
            jc.role.add(pub, chief)
        mc, create = Credits.objects.get_or_create(issue=i, creator=marie)
        if create:
            mc.role.add(eic)


add_dc_credits.short_description = "Add current DC executive credits"


def add_marvel_credits(modeladmin, request, queryset):
    cb = Creator.objects.get(slug="c-b-cebulski")
    eic = Role.objects.get(name__iexact="editor in chief")
    for i in queryset:
        cred, create = Credits.objects.get_or_create(issue=i, creator=cb)
        if create:
            cred.role.add(eic)


add_marvel_credits.short_description = "Add current Marvel EIC"


@admin.register(Arc)
class ArcAdmin(AdminImageMixin, SimpleHistoryAdmin):
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    field = ("name", "slug", "desc", "image")


@admin.register(Character)
class CharacterAdmin(AdminImageMixin, SimpleHistoryAdmin):
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    # form view
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "desc",
                    "wikipedia",
                    "alias",
                    "image",
                    "edited_by",
                )
            },
        ),
        ("Related", {"fields": ("creators", "teams")}),
    )
    filter_horizontal = ("creators", "teams")


@admin.register(Creator)
class CreatorAdmin(AdminImageMixin, SimpleHistoryAdmin):
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("modified",)
    field = ("name", "slug", "modified", "birth", "death", "desc", "wikipedia", "image")


@admin.register(Issue)
class IssueAdmin(AdminImageMixin, SimpleHistoryAdmin):
    form = IssueForm
    search_fields = ("series__name",)
    list_display = ("__str__", "cover_date", "store_date")
    list_filter = (
        FutureStoreDateListFilter,
        "created_on",
        "modified",
        "store_date",
        "cover_date",
        "series__publisher",
    )
    list_select_related = ("series",)
    date_hierarchy = "cover_date"
    actions = [add_dc_credits, add_marvel_credits]
    actions_on_top = True
    # form view
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "series",
                    "number",
                    "name",
                    "slug",
                    "cover_date",
                    "store_date",
                    "price",
                    "sku",
                    "upc",
                    "page",
                    "desc",
                    "image",
                    "created_by",
                    "edited_by",
                )
            },
        ),
        ("Related", {"fields": ("characters", "teams", "arcs")}),
    )
    filter_horizontal = ("arcs", "characters", "teams")
    inlines = (CreditsInline, VariantInline)


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


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    readonly_fields = ("modified",)
    fields = ("name", "notes", "order", "modified")


class SeriesAdminForm(ModelForm):
    class Meta:
        model = Series
        exclude = ()
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "sort_name": TextInput(attrs={"class": "input"}),
            "volume": TextInput(attrs={"class": "input"}),
            "year_began": TextInput(attrs={"class": "input"}),
            "year_end": TextInput(attrs={"class": "input"}),
            "series_type": Select(),
            "associated": SearchableSelect(
                model="comicsdb.Series", search_field="name", many=True, limit=200
            ),
            "publisher": Select(),
            "desc": Textarea(attrs={"class": "textarea"}),
        }
        help_texts = {
            "sort_name": """Most of the time it will be the same as the series name,
            but if the title starts with an article like 'The' it might be remove so
            that it is listed with like named series.""",
            "year_end": "Leave blank if a One-Shot, Annual, or Ongoing Series.",
            "associated": "Associate a series with another. For example an annual with it's primary series.",
        }
        labels = {"associated": "Associated Series"}


@admin.register(Series)
class SeriesAdmin(SimpleHistoryAdmin):
    form = SeriesAdminForm
    search_fields = ("name",)
    list_display = ("name", "year_began")
    list_filter = ("modified", "publisher")
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
        "associated",
        "desc",
        "edited_by",
    )


@admin.register(SeriesType)
class SeriesTypeAdmin(admin.ModelAdmin):
    fields = ("name", "notes")


@admin.register(Team)
class TeamAdmin(AdminImageMixin, SimpleHistoryAdmin):
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    # form view
    fieldsets = (
        (None, {"fields": ("name", "slug", "desc", "wikipedia", "image", "edited_by")}),
        ("Related", {"fields": ("creators",)}),
    )
    filter_horizontal = ("creators",)
