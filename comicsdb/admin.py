from django.contrib import admin

from comicsdb.models import Publisher


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'series_count',)
    readonly_fields = ('modified',)
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'modified', 'founded', 'short_desc', 'desc', 'image')
        }),
    )
