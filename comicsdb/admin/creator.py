from django.contrib import admin, messages
from django.utils.translation import ngettext
from sorl.thumbnail.admin.current import AdminImageMixin

from comicsdb.admin.util import AttributionInline
from comicsdb.models import Creator


@admin.register(Creator)
class CreatorAdmin(AdminImageMixin, admin.ModelAdmin):
    search_fields = ("name", "alias")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("created_on", "modified")
    readonly_fields = ("modified",)
    field = ("name", "slug", "modified", "birth", "death", "alias", "desc", "image")
    inlines = [AttributionInline]

    @admin.action(description="Remove bad creator images")
    def remove_bad_image(self, request, queryset) -> None:
        count = 0
        for i in queryset:
            if i.image == "0":
                i.image = ""
                i.save()
                count += 1

        self.message_user(
            request,
            ngettext(
                "%d creator image was fixed.",
                "%d creators images were fixed.",
                count,
            )
            % count,
            messages.SUCCESS,
        )
