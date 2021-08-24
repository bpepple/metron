from django.forms import ClearableFileInput, ModelForm, Textarea, TextInput

from comicsdb.models import Arc


class ArcForm(ModelForm):
    class Meta:
        model = Arc
        exclude = ("edited_by", "slug")
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "desc": Textarea(attrs={"class": "textarea"}),
            "image": ClearableFileInput(),
        }
