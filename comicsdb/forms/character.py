from django.forms import (ModelForm, TextInput, Textarea,
                          ClearableFileInput, SelectMultiple)

from comicsdb.models import Character


class CharacterForm(ModelForm):

    class Meta:
        model = Character
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'input'}),
            'slug': TextInput(attrs={'class': 'input'}),
            'desc': Textarea(attrs={'class': 'textarea'}),
            'creator': SelectMultiple(),
            'image': ClearableFileInput(),
        }
