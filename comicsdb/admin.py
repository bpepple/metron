from django.contrib import admin

from comicsdb.models import (Creator, Issue, Publisher,
                             Role, Series, SeriesType)


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name')
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    readonly_fields = ('modified',)
    field = ('first_name', 'last_name', 'slug', 'modified',
             'birth', 'death', 'desc', 'image')


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    search_fields = ('series__name',)
    list_display = ('__str__',)
    list_filter = ('cover_date',)
    list_select_related = ('series',)
    date_hierarchy = 'cover_date'
    fields = ('series', 'number', 'name', 'slug',
              'cover_date', 'store_date', 'desc', 'image')

    def get_queryset(self, request):
        queryset = (
            Issue.objects
            .select_related('series')
        )
        return queryset


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'series_count',)
    readonly_fields = ('modified',)
    fields = ('name', 'slug', 'modified', 'founded', 'short_desc',
              'desc', 'image')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    readonly_fields = ('modified',)
    fields = ('name', 'notes', 'modified')


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'year_began')
    list_filter = ('publisher',)
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'sort_name', 'publisher', 'volume',
              'year_began', 'year_end', 'series_type', 'short_desc', 'desc')


@admin.register(SeriesType)
class SeriesTypeAdmin(admin.ModelAdmin):
    fields = ('name', 'notes')
