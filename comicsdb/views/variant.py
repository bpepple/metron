from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic.edit import CreateView

from comicsdb.forms.variant import VariantForm
from comicsdb.models import Issue, Variant


class VariantCreate(LoginRequiredMixin, CreateView):
    model = Variant
    form_class = VariantForm
    template_name = "comicsdb/model_with_image_form.html"

    def get_success_url(self):
        slug = self.kwargs.get("slug", self.request.POST.get("slug"))

        return reverse("issue:detail", kwargs={"slug": slug})

    def get_context_data(self, **kwargs):
        context = super(VariantCreate, self).get_context_data(**kwargs)
        context["title"] = f"Add variant cover to {self.issue}"
        return context

    def get_initial(self):
        """Calculate Initial Data for the form, validate ownership of issue """
        slug = self.kwargs.get("slug", self.request.POST.get("slug"))
        self.issue = Issue.objects.select_related("series").get(slug=slug)

        return {"issue": self.issue}
