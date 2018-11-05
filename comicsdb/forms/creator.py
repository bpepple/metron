import datetime

from django.forms import (ModelForm, TextInput, Textarea,
                          ClearableFileInput, SelectDateWidget)

from comicsdb.models import Creator


YEARS = [(r) for r in range(1900, datetime.date.today().year)]


class CreatorForm(ModelForm):

    class Meta:
        model = Creator
        fields = '__all__'
        widgets = {
            'first_name': TextInput(attrs={'class': 'input'}),
            'last_name': TextInput(attrs={'class': 'input'}),
            'slug': TextInput(attrs={'class': 'input'}),
            'desc': Textarea(attrs={'class': 'textarea'}),
            'birth': SelectDateWidget(attrs={'class': 'input', 'style': 'width: 10%; display: inline-block;'},
                                      empty_label=("Choose Year", "Choose Month", "Choose Day"),
                                      years=YEARS),
            'death': SelectDateWidget(attrs={'class': 'input', 'style': 'width: 10%; display: inline-block;'},
                                      empty_label=("Choose Year", "Choose Month", "Choose Day"),
                                      years=YEARS),
            'image': ClearableFileInput(),
        }
