from django.forms import ClearableFileInput, ModelForm, Textarea, TextInput

from comicsdb.models import Publisher


class PublisherForm(ModelForm):
    class Meta:
        model = Publisher
        exclude = ("edited_by", "slug")
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "short_desc": TextInput(attrs={"class": "input"}),
            "desc": Textarea(attrs={"class": "textarea"}),
            "wikipedia": TextInput(attrs={"class": "input"}),
            "founded": TextInput(attrs={"class": "input"}),
            "image": ClearableFileInput(),
        }
        help_texts = {
            "wikipedia": "If the description is from wikipedia, please supply that pages slug"
            + " so we can provide attribution to them."
        }
