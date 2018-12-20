from django.forms import ModelForm, inlineformset_factory, ModelChoiceField

from comicsdb.models import Credits, Issue, Creator
from dal import autocomplete


class CreditsForm(ModelForm):
    creator = ModelChoiceField(
        queryset=Creator.objects.all(),
        widget=autocomplete.ModelSelect2(url='issue:creator-autocomplete',
                                         attrs={
                                             'data-placeholder': 'Autocomplete...',
                                             'data-minimum-input-length': 3
                                         },)
    )

    class Meta:
        model = Credits
        fields = '__all__'


CreditsFormSet = inlineformset_factory(Issue, Credits, form=CreditsForm,
                                       extra=1)
