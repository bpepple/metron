from django.forms import ClearableFileInput, ModelForm, TextInput, inlineformset_factory

from comicsdb.models import Variant
from comicsdb.models.issue import Issue


class VariantForm(ModelForm):
    class Media:
        css = {"all": ("admin/css/widgets.css",)}
        js = (("/jsi18n"),)

    class Meta:
        model = Variant
        fields = ("image", "name", "sku", "upc")
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "sku": TextInput(attrs={"class": "input"}),
            "upc": TextInput(attrs={"class": "input"}),
            "image": ClearableFileInput(),
        }


VariantFormset = inlineformset_factory(
    Issue, Variant, form=VariantForm, extra=3, can_delete=True
)
