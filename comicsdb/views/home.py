from datetime import datetime

from django.views.generic.base import TemplateView

from comicsdb.models import Issue


class HomePageView(TemplateView):
    template_name = "comicsdb/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        updated = datetime.now()
        context["updated"] = updated
        context["recently_edited"] = (
            Issue.objects.prefetch_related("series", "series__series_type")
            .order_by("-modified")
            .all()[:12]
        )

        return context
