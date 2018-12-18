from django.forms import ModelForm, inlineformset_factory

from comicsdb.models import Credits, Issue


class CreditsForm(ModelForm):

    class Meta:
        model = Credits
        fields = '__all__'

CreditsFormSet = inlineformset_factory(Issue, Credits, form=CreditsForm,
                                       extra=1)
