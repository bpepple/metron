from dal import autocomplete
from django.forms import ModelChoiceField, ModelForm, SelectMultiple, inlineformset_factory

from comicsdb.models import Creator, Credits, Issue


class CreditsForm(ModelForm):
    creator = ModelChoiceField(
        queryset=Creator.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="issue:creator-autocomplete",
            attrs={
                "data-placeholder": "Autocomplete...",
                "data-minimum-input-length": 3,
            },
        ),
    )

    class Meta:
        model = Credits
        fields = "__all__"
        widgets = {"role": SelectMultiple(attrs={"size": 6})}


CreditsFormSet = inlineformset_factory(
    Issue, Credits, form=CreditsForm, extra=1, can_delete=True
)
