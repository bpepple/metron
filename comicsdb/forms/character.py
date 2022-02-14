from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ClearableFileInput, ModelForm, Textarea, TextInput

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
            "creators": FilteredSelectMultiple(
                "Creators", attrs={"size": "6"}, is_stacked=False
            ),
            "teams": FilteredSelectMultiple("Teams", attrs={"size": "6"}, is_stacked=False),
            "image": ClearableFileInput(),
        }
        help_texts = {
            "alias": "Separate multiple aliases by a comma",
        }
