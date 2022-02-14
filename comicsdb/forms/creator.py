from django.forms import ClearableFileInput, DateInput, ModelForm, Textarea, TextInput

from comicsdb.models import Creator


class CreatorForm(ModelForm):
    class Meta:
        model = Creator
        fields = (
            "name",
            "desc",
            "alias",
            "birth",
            "death",
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
            "image": ClearableFileInput(),
        }
        help_texts = {
            "alias": "Separate multiple aliases by a comma",
        }
