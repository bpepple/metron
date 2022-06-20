from django.views.generic.base import TemplateView

from comicsdb.models import Arc, Character, Creator, Issue, Publisher, Series, Team


class HomePageView(TemplateView):
    template_name = "comicsdb/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["publisher"] = Publisher.objects.count()
        context["series"] = Series.objects.count()
        context["issue"] = Issue.objects.count()
        context["character"] = Character.objects.count()
        context["creator"] = Creator.objects.count()
        context["team"] = Team.objects.count()
        context["arc"] = Arc.objects.count()
        context["recently_edited"] = (
            Issue.objects.prefetch_related("series", "series__series_type")
            .order_by("-modified")
            .all()[:12]
        )

        return context
