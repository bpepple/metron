from django.contrib import admin

from comicsdb.models import Publisher, Series, SeriesType


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'series_count',)
    readonly_fields = ('modified',)
    fields = ('name', 'slug', 'modified', 'founded', 'short_desc',
              'desc', 'image')


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'year_began')
    list_filter = ('publisher',)
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'sort_name', 'publisher', 'volume',
              'year_began', 'year_end', 'type', 'short_desc', 'desc')


@admin.register(SeriesType)
class SeriesTypeAdmin(admin.ModelAdmin):
    fields = ('name', 'notes')
