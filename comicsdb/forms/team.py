from django.forms import (ModelForm, TextInput, Textarea, ClearableFileInput)
from django.contrib.admin.widgets import FilteredSelectMultiple

from comicsdb.models import Team


class TeamForm(ModelForm):

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/jsi18n'),

    class Meta:
        model = Team
        fields = ('name', 'slug', 'desc', 'wikipedia', 'creators', 'image')
        widgets = {
            'name': TextInput(attrs={'class': 'input'}),
            'slug': TextInput(attrs={'class': 'input'}),
            'desc': Textarea(attrs={'class': 'textarea'}),
            'wikipedia': TextInput(attrs={'class': 'input'}),
            'creators': FilteredSelectMultiple("Creators", attrs={'size': '6'}, is_stacked=False),
            'image': ClearableFileInput(),
        }
        help_texts = {
            'wikipedia': 'If the description is from wikipedia, please supply that pages slug' +
                         ' so we can provide attribution to them.'
        }
