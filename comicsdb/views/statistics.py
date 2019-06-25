from django.db.models import Count
from django.views.generic.base import TemplateView

from comicsdb.models import Publisher


class StatisticsView(TemplateView):
    template_name = "comicsdb/statistics.html"

    def get_context_data(self, **kwargs):
        context = super(StatisticsView, self).get_context_data(**kwargs)
        data = Publisher.objects.annotate(num_issues=Count("series__issue")).values(
            "name", "num_issues"
        )

        count_dict = {}
        for pub in data:
            count_dict.update({pub["name"]: pub["num_issues"]})
        context["pub_issues"] = count_dict

        return context
