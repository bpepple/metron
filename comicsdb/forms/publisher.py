from django.forms import (ModelForm, TextInput, Textarea, ClearableFileInput)

from comicsdb.models import Publisher


class PublisherForm(ModelForm):

    class Meta:
        model = Publisher
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'input'}),
            'slug': TextInput(attrs={'class': 'input'}),
            'short_desc': TextInput(attrs={'class': 'input'}),
            'desc': Textarea(attrs={'class': 'textarea'}),
            'founded': TextInput(attrs={'class': 'input'}),
            'image': ClearableFileInput(),
        }
