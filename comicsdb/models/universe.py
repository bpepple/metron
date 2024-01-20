import contextlib
import logging

from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save
from sorl.thumbnail import ImageField

from comicsdb.models import Attribution, Publisher
from comicsdb.models.common import CommonInfo, pre_save_slug
from users.models import CustomUser

LOGGER = logging.getLogger(__name__)


class Universe(CommonInfo):
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    image = ImageField(upload_to="universe/%Y/%m/%d/", blank=True)
    designation = models.CharField(max_length=255, blank=True)
    attribution = GenericRelation(Attribution, related_query_name="universes")
    edited_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)

    def save(self, *args, **kwargs) -> None:
        # Let's delete the original image if we're replacing it by uploading a new one.
        with contextlib.suppress(ObjectDoesNotExist):
            this = Universe.objects.get(id=self.id)
            if this.image and this.image != self.image:
                LOGGER.info(
                    f"Replacing {this.image} with {img if (img := self.image) else 'None'}."
                )

                this.image.delete(save=False)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        pass

    @property
    def wikipedia(self):
        return self.attribution.filter(source=Attribution.Source.WIKIPEDIA)

    @property
    def marvel(self):
        return self.attribution.filter(source=Attribution.Source.MARVEL)

    @property
    def universe_name(self) -> str:
        if self.designation and self.name != self.designation:
            return f"{self.name} — {self.designation}"
        return self.name

    def __str__(self) -> str:
        return f"{self.publisher}: {self.universe_name}"

    class Meta:
        indexes = [models.Index(fields=["name"], name="universe_name_idx")]
        ordering = ["name", "designation"]
        db_table_comment = "Publisher Universes"


pre_save.connect(pre_save_slug, sender=Universe, dispatch_uid="pre_save_universe")
