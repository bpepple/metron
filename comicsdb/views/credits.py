from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from comicsdb.forms.credits import CreditsForm
from comicsdb.models import Credits, Issue


class CreditsCreate(CreateView):
    model = Credits
    form_class = CreditsForm
    template_name = 'comicsdb/credits_form.html'

    def get_success_url(self):
        slug = self.kwargs.get('slug', self.request.POST.get('slug'))

        return reverse('issue:detail', kwargs={'slug': slug})

    def get_initial(self):
        """Calculate Initial Data for the form, validate ownership of issue """
        issue_slug = self.kwargs.get('slug', self.request.POST.get('slug'))
        issue = get_object_or_404(Issue, slug=issue_slug)

        return {'issue_slug': issue_slug}
