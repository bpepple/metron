from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from sorl.thumbnail import ImageField

from users.models import CustomUser

from .common import CommonInfo, pre_save_slug


class Publisher(CommonInfo):
    founded = models.PositiveSmallIntegerField("Year Founded", null=True, blank=True)
    wikipedia = models.CharField("Wikipedia Slug", max_length=255, blank=True)
    image = ImageField("Logo", upload_to="publisher/%Y/%m/%d/", blank=True)
    edited_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)

    def get_absolute_url(self):
        return reverse("publisher:detail", args=[self.slug])

    @property
    def series_count(self):
        return self.series_set.all().count()

    def __str__(self) -> str:
        return self.name


pre_save.connect(pre_save_slug, sender=Publisher, dispatch_uid="pre_save_publisher")
