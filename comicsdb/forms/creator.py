import datetime

from django.forms import (
    ClearableFileInput,
    ModelForm,
    SelectDateWidget,
    Textarea,
    TextInput,
)

from comicsdb.models import Creator

YEARS = [(r) for r in range(1890, datetime.date.today().year + 1)]


class CreatorForm(ModelForm):
    class Meta:
        model = Creator
        fields = (
            "name",
            "slug",
            "desc",
            "wikipedia",
            "alias",
            "birth",
            "death",
            "image",
        )
        exclude = ("edited_by",)
        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "slug": TextInput(attrs={"class": "input"}),
            "desc": Textarea(attrs={"class": "textarea"}),
            "wikipedia": TextInput(attrs={"class": "input"}),
            "alias": TextInput(attrs={"class": "input"}),
            "birth": SelectDateWidget(
                attrs={"class": "input", "style": "width: 10%; display: inline-block;"},
                empty_label=("Choose Year", "Choose Month", "Choose Day"),
                years=YEARS,
            ),
            "death": SelectDateWidget(
                attrs={"class": "input", "style": "width: 10%; display: inline-block;"},
                empty_label=("Choose Year", "Choose Month", "Choose Day"),
                years=YEARS,
            ),
            "image": ClearableFileInput(),
        }
        help_texts = {
            "wikipedia": "If the description is from wikipedia, please supply that pages slug"
            + " so we can provide attribution to them.",
            "alias": "Separate multiple aliases by a comma",
        }
