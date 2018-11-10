from django.forms import (ModelForm, TextInput, Textarea,
                          ClearableFileInput, SelectDateWidget)

from comicsdb.models import Team


class TeamForm(ModelForm):

    class Meta:
        model = Team
        fields = ('name', 'slug', 'desc', 'wikipedia', 'image')
        widgets = {
            'name': TextInput(attrs={'class': 'input'}),
            'slug': TextInput(attrs={'class': 'input'}),
            'desc': Textarea(attrs={'class': 'textarea'}),
            'wikipedia': TextInput(attrs={'class': 'input'}),
            'image': ClearableFileInput(),
        }
        help_texts = {
            'wikipedia': 'If the description is from wikipedia, please supply that pages slug' +
                         ' so we can provide attribution to them.'
        }
