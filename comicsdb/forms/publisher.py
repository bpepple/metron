from django.forms import ModelForm, TextInput, Textarea, ClearableFileInput

from comicsdb.models import Publisher


class PublisherForm(ModelForm):
    class Meta:
        model = Publisher
        exclude = ("edited_by",)
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "slug": TextInput(attrs={"class": "input"}),
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
