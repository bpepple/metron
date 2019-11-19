from django.forms import ClearableFileInput, DateInput, ModelForm, Textarea, TextInput

from comicsdb.models import Creator


class CreatorForm(ModelForm):
    class Meta:
        model = Creator
        fields = (
            "name",
            "slug",
            "desc",
            "wikipedia",
            "alias",
            "birth",
            "death",
            "image",
        )
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "slug": TextInput(attrs={"class": "input"}),
            "desc": Textarea(attrs={"class": "textarea"}),
            "wikipedia": TextInput(attrs={"class": "input"}),
            "alias": TextInput(attrs={"class": "input"}),
            "birth": DateInput(attrs={"class": "input", "type": "date"},),
            "death": DateInput(attrs={"class": "input", "type": "date"},),
            "image": ClearableFileInput(),
        }
        help_texts = {
            "wikipedia": "If the description is from wikipedia, please supply that pages slug so we can provide attribution to them.",
            "alias": "Separate multiple aliases by a comma",
        }
