from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import (ModelForm, TextInput, Textarea, ClearableFileInput)

from comicsdb.models import Character, Creator


class CharacterForm(ModelForm):

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n'),

    class Meta:
        model = Character
        fields = ('name', 'slug', 'desc', 'wikipedia',
                  'creators', 'teams', 'image')
        widgets = {
            'name': TextInput(attrs={'class': 'input'}),
            'slug': TextInput(attrs={'class': 'input'}),
            'desc': Textarea(attrs={'class': 'textarea'}),
            'wikipedia': TextInput(attrs={'class': 'input'}),
            'creators': FilteredSelectMultiple("Creators", is_stacked=False),
            'teams': FilteredSelectMultiple("Teams", is_stacked=False),
            'image': ClearableFileInput(),
        }
        help_texts = {
            'wikipedia': 'If the description is from wikipedia, please supply that pages slug' +
                         ' so we can provide attribution to them.'
        }