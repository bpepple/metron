import logging

from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from sorl.thumbnail import ImageField

from users.models import CustomUser

from .attribution import Attribution
from .common import CommonInfo, pre_save_slug

LOGGER = logging.getLogger(__name__)


class Publisher(CommonInfo):
    founded = models.PositiveSmallIntegerField("Year Founded", null=True, blank=True)
    image = ImageField("Logo", upload_to="publisher/%Y/%m/%d/", blank=True)
    attribution = GenericRelation(Attribution, related_query_name="publishers")
    edited_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)

    def save(self, *args, **kwargs) -> None:
        # Let's delete the original image if we're replacing it by uploading a new one.
        try:
            this = Publisher.objects.get(id=self.id)
            if this.image and this.image != self.image:
                LOGGER.info(
                    f"Replacing {this.image} with {'None' if not(img:=self.image) else img}."
                )
                this.image.delete(save=False)
        except ObjectDoesNotExist:
            pass
        return super(Publisher, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("publisher:detail", args=[self.slug])

    @property
    def series_count(self):
        return self.series_set.all().count()

    @property
    def wikipedia(self):
        return self.attribution.filter(source=Attribution.Source.WIKIPEDIA)

    @property
    def marvel(self):
        return self.attribution.filter(source=Attribution.Source.MARVEL)

    def __str__(self) -> str:
        return self.name


pre_save.connect(pre_save_slug, sender=Publisher, dispatch_uid="pre_save_publisher")
