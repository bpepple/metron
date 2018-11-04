from django.forms import ModelForm, Select, SelectMultiple, CharField, HiddenInput

from comicsdb.models import Credits, Issue


class CreditsForm(ModelForm):

    class Meta:
        model = Credits
        fields = '__all__'
        widgets = {
            'issue': Select(),
            'creator': Select(),
            'role': SelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(CreditsForm, self).__init__(*args, **kwargs)

        issue = Issue.objects.get(slug=kwargs["initial"]["issue_slug"])
        self.initial['issue'] = issue
