from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm, Select

from comicsdb.models import Credits, Issue


class CreditsForm(ModelForm):

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n'),

    class Meta:
        model = Credits
        fields = '__all__'
        widgets = {
            'issue': Select(),
            'creator': Select(),
            'role': FilteredSelectMultiple("Roles", attrs={'size': '6'}, is_stacked=False)
        }

    def __init__(self, *args, **kwargs):
        super(CreditsForm, self).__init__(*args, **kwargs)

        issue = Issue.objects.get(slug=kwargs["initial"]["issue_slug"])
        self.initial['issue'] = issue
