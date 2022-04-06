import itertools

from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify

from comicsdb.models.attribution import Attribution
from users.models import CustomUser

from .common import CommonInfo
from .publisher import Publisher


class SeriesType(models.Model):
    name = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class Series(CommonInfo):
    sort_name = models.CharField(max_length=255)
    volume = models.PositiveSmallIntegerField("Volume Number")
    year_began = models.PositiveSmallIntegerField("Year Began")
    year_end = models.PositiveSmallIntegerField("Year Ended", null=True, blank=True)
    series_type = models.ForeignKey(SeriesType, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    associated = models.ManyToManyField("self", blank=True)
    attribution = GenericRelation(Attribution, related_query_name="series")
    edited_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)

    def get_absolute_url(self):
        return reverse("series:detail", args=[self.slug])

    def __str__(self) -> str:
        try:
            if self.series_type.name == "Trade Paper Back":
                return f"{self.name} TPB ({self.year_began})"
            else:
                return f"{self.name} ({self.year_began})"
        except ObjectDoesNotExist:
            return "New"

    def first_issue_cover(self):
        try:
            return self.issue_set.all().first().image
        except AttributeError:
            return None

    @property
    def issue_count(self) -> int:
        return self.issue_set.all().count()

    class Meta:
        verbose_name_plural = "Series"
        unique_together = ["publisher", "name", "volume", "series_type"]
        ordering = ["sort_name", "year_began"]


def generate_series_slug(instance):
    slug_candidate = slug_original = slugify(f"{instance.name}-{instance.year_began}")
    Klass = instance.__class__
    for i in itertools.count(1):
        if not Klass.objects.filter(slug=slug_candidate).exists():
            break
        slug_candidate = f"{slug_original}-{i}"

    return slug_candidate


def pre_save_series_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = generate_series_slug(instance)


pre_save.connect(pre_save_series_slug, sender=Series, dispatch_uid="pre_save_series")
