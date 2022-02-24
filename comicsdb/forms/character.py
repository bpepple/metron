from django.forms import ClearableFileInput, ModelForm, Textarea, TextInput

from comicsdb.forms.creator import CreatorsWidget
from comicsdb.forms.team import TeamsWidget
from comicsdb.models import Character


class CharacterForm(ModelForm):
    class Media:
        css = {"all": ("admin/css/widgets.css",)}
        js = (("/jsi18n"),)

    class Meta:
        model = Character
        fields = (
            "name",
            "desc",
            "alias",
            "creators",
            "teams",
            "image",
        )
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "desc": Textarea(attrs={"class": "textarea"}),
            "alias": TextInput(attrs={"class": "input"}),
            "creators": CreatorsWidget(attrs={"class": "input"}),
            "teams": TeamsWidget(attrs={"class": "input"}),
            "image": ClearableFileInput(),
        }
        help_texts = {
            "alias": "Separate multiple aliases by a comma",
        }
