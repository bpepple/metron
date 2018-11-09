from django.forms import (ModelForm, TextInput, Textarea,
                          SelectMultiple, ClearableFileInput)

from comicsdb.models import Character


class CharacterForm(ModelForm):

    class Meta:
        model = Character
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'input'}),
            'slug': TextInput(attrs={'class': 'input'}),
            'desc': Textarea(attrs={'class': 'textarea'}),
            'wikipedia': TextInput(attrs={'class': 'input'}),
            'creator': SelectMultiple(),
            'image': ClearableFileInput(),
        }
        help_texts = {
            'wikipedia': 'If the description is from wikipedia, please supply that pages slug' +
                         ' so we can provide attribution to them.'
        }
