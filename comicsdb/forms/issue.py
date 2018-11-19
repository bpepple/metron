import datetime

from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import (ModelForm, TextInput, Textarea, Select,
                          SelectDateWidget, ClearableFileInput)

from comicsdb.models import Issue


YEARS = [(r) for r in range(1925, datetime.date.today().year + 2)]


class IssueForm(ModelForm):

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n'),

    class Meta:
        model = Issue
        # exclude 'creators' field
        fields = ('series', 'name', 'slug', 'number', 'cover_date',
                  'store_date', 'desc', 'characters', 'arcs', 'teams',
                  'image')
        widgets = {
            'series': Select(),
            'name': TextInput(attrs={'class': 'input'}),
            'slug': TextInput(attrs={'class': 'input'}),
            'number': TextInput(attrs={'class': 'input'}),
            'arcs': FilteredSelectMultiple("Story Arcs", attrs={'size': '6'}, is_stacked=False),
            'characters': FilteredSelectMultiple("Characters", attrs={'size': '6'}, is_stacked=False),
            'teams': FilteredSelectMultiple("Teams", attrs={'size': '6'}, is_stacked=False),
            'cover_date': SelectDateWidget(attrs={'class': 'input', 'style': 'width: 10%; display: inline-block;'},
                                           empty_label=(
                                               "Choose Year", "Choose Month", "Choose Day"),
                                           years=YEARS),
            'store_date': SelectDateWidget(attrs={'class': 'input', 'style': 'width: 10%; display: inline-block;'},
                                           empty_label=(
                                               "Choose Year", "Choose Month", "Choose Day"),
                                           years=YEARS),
            'desc': Textarea(attrs={'class': 'textarea'}),
            'image': ClearableFileInput(),
        }
