from django.forms import ClearableFileInput, ModelForm, Textarea, TextInput

from comicsdb.models import Arc


class ArcForm(ModelForm):
    class Meta:
        model = Arc
        fields = ("name", "desc", "cv_id", "image")
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "cv_id": TextInput(attrs={"class": "input"}),
            "desc": Textarea(attrs={"class": "textarea"}),
            "image": ClearableFileInput(),
        }
