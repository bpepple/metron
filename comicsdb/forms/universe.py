from django.forms import ClearableFileInput, ModelForm
from django_select2 import forms as s2forms

from comicsdb.models import Universe


class UniversesWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = ["name__icontains", "designation__icontains"]


class UniverseForm(ModelForm):
    class Meta:
        model = Universe
        fields = ("publisher", "name", "designation", "desc", "image")
        widgets = {"image": ClearableFileInput()}
