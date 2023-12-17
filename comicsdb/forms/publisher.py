from django.forms import ClearableFileInput, ModelForm

from comicsdb.models import Publisher


class PublisherForm(ModelForm):
    class Meta:
        model = Publisher
        fields = ["name", "desc", "founded", "cv_id", "image"]
        widgets = {
            "image": ClearableFileInput(),
        }

    field_order = ["name", "desc", "founded", "cv_id", "image"]
