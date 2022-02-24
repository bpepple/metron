from django.forms import ClearableFileInput, ModelForm, Textarea, TextInput
from django_select2 import forms as s2forms

from comicsdb.forms.creator import CreatorsWidget
from comicsdb.models import Team


class TeamsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = ["name__icontains"]


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
            "creators": CreatorsWidget(attrs={"class": "input"}),
            "image": ClearableFileInput(),
        }
