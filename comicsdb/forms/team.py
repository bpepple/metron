from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ClearableFileInput, ModelForm, Textarea, TextInput

from comicsdb.models import Team


class TeamForm(ModelForm):
    class Media:
        css = {"all": ("admin/css/widgets.css",)}
        js = (("/jsi18n"),)

    class Meta:
        model = Team
        fields = ("name", "desc", "creators", "image")
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "desc": Textarea(attrs={"class": "textarea"}),
            "creators": FilteredSelectMultiple(
                "Creators", attrs={"size": "6"}, is_stacked=False
            ),
            "image": ClearableFileInput(),
        }
