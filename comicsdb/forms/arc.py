from django.forms import ModelForm, TextInput, Textarea, ClearableFileInput

from comicsdb.models import Arc


class ArcForm(ModelForm):
    class Meta:
        model = Arc
        exclude = ("edited_by",)
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "slug": TextInput(attrs={"class": "input"}),
            "desc": Textarea(attrs={"class": "textarea"}),
            "image": ClearableFileInput(),
        }
