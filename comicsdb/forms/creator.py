from django.forms import ClearableFileInput, DateInput, ModelForm, Textarea, TextInput
from django_select2 import forms as s2forms

from comicsdb.models import Creator


class CreatorsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
        "alias__icontains",
    ]


class CreatorForm(ModelForm):
    class Meta:
        model = Creator
        fields = (
            "name",
            "desc",
            "alias",
            "birth",
            "death",
            "cv_id",
            "image",
        )
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "desc": Textarea(attrs={"class": "textarea"}),
            "alias": TextInput(attrs={"class": "input"}),
            "birth": DateInput(
                attrs={"class": "input", "type": "date"},
            ),
            "death": DateInput(
                attrs={"class": "input", "type": "date"},
            ),
            "cv_id": TextInput(attrs={"class": "input"}),
            "image": ClearableFileInput(),
        }
        help_texts = {
            "alias": "Separate multiple aliases by a comma",
        }
