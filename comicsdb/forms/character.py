from django.forms import ClearableFileInput, ModelForm

from comicsdb.forms.creator import CreatorsWidget
from comicsdb.forms.team import TeamsWidget
from comicsdb.models import Character


class CharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = (
            "name",
            "desc",
            "alias",
            "creators",
            "teams",
            "cv_id",
            "image",
        )
        widgets = {
            "creators": CreatorsWidget(attrs={"class": "input"}),
            "teams": TeamsWidget(attrs={"class": "input"}),
            "image": ClearableFileInput(),
        }
        help_texts = {
            "alias": "Separate multiple aliases by a comma",
        }
