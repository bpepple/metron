from django.contrib.contenttypes.admin import GenericStackedInline

from comicsdb.models.attribution import Attribution


class AttributionInline(GenericStackedInline):
    model = Attribution
    extra = 1
