from django.forms import ClearableFileInput, HiddenInput, ModelForm, TextInput

from comicsdb.models import Issue, Variant


class VariantForm(ModelForm):
    class Media:
        css = {"all": ("admin/css/widgets.css",)}
        js = (("/jsi18n"),)

    class Meta:
        model = Variant
        fields = ("issue", "name", "image")
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "image": ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(VariantForm, self).__init__(*args, **kwargs)

        issue = Issue.objects.get(slug=kwargs["initial"]["issue_slug"])
        self.initial["issue"] = issue
        self.fields["issue"].widget = HiddenInput()
