from django.contrib.contenttypes.forms import (
    BaseGenericInlineFormSet,
    generic_inlineformset_factory,
)
from django.forms import ModelForm, TextInput

from comicsdb.models.attribution import Attribution


class AttributionForm(ModelForm):
    class Meta:
        model = Attribution
        fields = ["source", "url"]
        widgets = {
            "url": TextInput(attrs={"class": "input"}),
        }


AttributionFormSet = generic_inlineformset_factory(
    Attribution,
    AttributionForm,
    BaseGenericInlineFormSet,
    can_delete=True,
    extra=1,
)
