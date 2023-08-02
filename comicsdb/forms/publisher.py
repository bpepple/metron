from django.forms import ClearableFileInput, ModelForm, Textarea, TextInput

from comicsdb.models import Publisher


class PublisherForm(ModelForm):
    class Meta:
        model = Publisher
        fields = ["name", "desc", "founded", "cv_id", "image"]
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "desc": Textarea(attrs={"class": "textarea"}),
            "founded": TextInput(attrs={"class": "input"}),
            "cv_id": TextInput(attrs={"class": "input"}),
            "image": ClearableFileInput(),
        }

    field_order = ["name", "desc", "founded", "cv_id", "image"]
