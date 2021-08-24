from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ClearableFileInput, ModelForm, Textarea, TextInput

from comicsdb.models import Team


class TeamForm(ModelForm):
    class Media:
        css = {"all": ("admin/css/widgets.css",)}
        js = (("/jsi18n"),)

    class Meta:
        model = Team
        fields = ("name", "desc", "wikipedia", "creators", "image")
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "desc": Textarea(attrs={"class": "textarea"}),
            "wikipedia": TextInput(attrs={"class": "input"}),
            "creators": FilteredSelectMultiple(
                "Creators", attrs={"size": "6"}, is_stacked=False
            ),
            "image": ClearableFileInput(),
        }
        help_texts = {
            "wikipedia": "If the description is from wikipedia, please supply that pages slug"
            + " so we can provide attribution to them."
        }
