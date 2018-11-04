from django.forms import (ModelForm, TextInput, Textarea, Select,
                          SelectMultiple, SelectDateWidget, ClearableFileInput)
import datetime
from comicsdb.models import Issue

YEARS = [(r) for r in range(1925, datetime.date.today().year + 2)]


class IssueForm(ModelForm):

    class Meta:
        model = Issue
        exclude = ('creators',)
        widgets = {
            'series': Select(),
            'name': TextInput(attrs={'class': 'input'}),
            'slug': TextInput(attrs={'class': 'input'}),
            'number': TextInput(attrs={'class': 'input'}),
            'arcs': SelectMultiple(),
            'cover_date': SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),
                                           years=YEARS),
            'store_date': SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),
                                           years=YEARS),
            'desc': Textarea(attrs={'class': 'textarea'}),
            'image': ClearableFileInput(),
        }
