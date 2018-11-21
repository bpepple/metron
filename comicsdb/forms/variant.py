from django.forms import (ModelForm, TextInput, Select, ClearableFileInput)

from comicsdb.models import Variant, Issue


class VariantForm(ModelForm):

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n'),

    class Meta:
        model = Variant
        fields = ('issue', 'name', 'image')
        widgets = {
            'issue': Select(),
            'name': TextInput(attrs={'class': 'input'}),
            'image': ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(VariantForm, self).__init__(*args, **kwargs)

        issue = Issue.objects.get(slug=kwargs["initial"]["issue_slug"])
        self.fields['issue'].queryset = (
            Issue.objects
            .select_related('series')
        )
        self.initial['issue'] = issue
