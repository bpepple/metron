from django.forms import ClearableFileInput, HiddenInput, ModelForm, TextInput

from comicsdb.models import Variant


class VariantForm(ModelForm):
    class Media:
        css = {"all": ("admin/css/widgets.css",)}
        js = (("/jsi18n"),)

    class Meta:
        model = Variant
        fields = ("issue", "name", "sku", "upc", "image")
        widgets = {
            "issue": HiddenInput(),
            "name": TextInput(attrs={"class": "input"}),
            "sku": TextInput(attrs={"class": "input"}),
            "upc": TextInput(attrs={"class": "input"}),
            "image": ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(VariantForm, self).__init__(*args, **kwargs)
        # Set the issue
        self.initial["issue"] = kwargs["initial"]["issue"]
