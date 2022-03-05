import logging

from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from sorl.thumbnail import ImageField

from comicsdb.models.attribution import Attribution
from users.models import CustomUser

from .common import CommonInfo, pre_save_slug

LOGGER = logging.getLogger(__name__)


class Arc(CommonInfo):
    image = ImageField(upload_to="arc/%Y/%m/%d/", blank=True)
    attribution = GenericRelation(Attribution, related_query_name="arcs")
    edited_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)

    def save(self, *args, **kwargs) -> None:
        # Let's delete the original image if we're replacing it by uploading a new one.
        try:
            this = Arc.objects.get(id=self.id)
            if this.image and this.image != self.image:
                LOGGER.info(
                    f"Replacing {this.image} with {'None' if not(img:=self.image) else img}."
                )
                this.image.delete(save=False)
        except ObjectDoesNotExist:
            pass
        return super(Arc, self).save(*args, **kwargs)

    @property
    def issue_count(self):
        return self.issue_set.all().count()

    def get_absolute_url(self):
        return reverse("arc:detail", args=[self.slug])

    def __str__(self) -> str:
        return self.name


pre_save.connect(pre_save_slug, sender=Arc, dispatch_uid="pre_save_arc")
