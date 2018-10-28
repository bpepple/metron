import datetime

from django.forms import ModelForm, TextInput, Textarea, SelectDateWidget

from comicsdb.models import Publisher


YEARS = [(r) for r in range(1925, datetime.date.today().year + 1)]


class PublisherForm(ModelForm):

    class Meta:
        model = Publisher
        exclude = ['modified']
        widgets = {
            'name': TextInput(attrs={'class': 'input'}),
            'slug': TextInput(attrs={'class': 'input'}),
            'short_desc': TextInput(attrs={'class': 'input'}),
            'desc': Textarea(attrs={'class': 'textarea'}),
            'founded': SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),
                                        years=YEARS),
        }
