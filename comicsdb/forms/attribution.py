from django.contrib.contenttypes.forms import (
    BaseGenericInlineFormSet,
    generic_inlineformset_factory,
)
from django.forms import ModelForm

from comicsdb.models.attribution import Attribution


class AttributionForm(ModelForm):
    class Meta:
        model = Attribution
        fields = ["source", "url"]


AttributionFormSet = generic_inlineformset_factory(
    Attribution,
    AttributionForm,
    BaseGenericInlineFormSet,
    can_delete=True,
    extra=1,
)
