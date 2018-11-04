from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from comicsdb.forms.credits import CreditsForm
from comicsdb.models import Credits, Issue


class CreditsCreate(CreateView):
    model = Credits
    form_class = CreditsForm
    template_name = 'comicsdb/credits_form.html'
    # TODO: Need to reverse to the referring issue detail
    success_url = reverse_lazy('issue:list', kwargs={'page': 1})

    def get_initial(self):
        """Calculate Initial Data for the form, validate ownership of issue """
        issue_slug = self.kwargs.get('slug', self.request.POST.get('slug'))
        issue = get_object_or_404(Issue, slug=issue_slug)

        return {'issue_slug': issue_slug}
