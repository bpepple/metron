import contextlib
import logging

from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from sorl.thumbnail import ImageField

from comicsdb.models.attribution import Attribution
from comicsdb.models.common import CommonInfo, pre_save_slug
from comicsdb.models.creator import Creator
from comicsdb.models.universe import Universe
from users.models import CustomUser

LOGGER = logging.getLogger(__name__)


class Team(CommonInfo):
    image = ImageField(upload_to="team/%Y/%m/%d/", blank=True)
    creators = models.ManyToManyField(Creator, blank=True)
    universes = models.ManyToManyField(Universe, blank=True)
    attribution = GenericRelation(Attribution, related_query_name="teams")
    edited_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)

    def save(self, *args, **kwargs) -> None:
        # Let's delete the original image if we're replacing it by uploading a new one.
        with contextlib.suppress(ObjectDoesNotExist):
            this = Team.objects.get(id=self.id)
            if this.image and this.image != self.image:
                LOGGER.info(
                    f"Replacing {this.image} with {img if (img:=self.image) else 'None'}."
                )

                this.image.delete(save=False)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("team:detail", args=[self.slug])

    @property
    def issue_count(self):
        return self.issue_set.all().count()

    @property
    def wikipedia(self):
        return self.attribution.filter(source=Attribution.Source.WIKIPEDIA)

    @property
    def marvel(self):
        return self.attribution.filter(source=Attribution.Source.MARVEL)

    def __str__(self) -> str:
        return self.name

    class Meta:
        indexes = [models.Index(fields=["name"], name="team_name_idx")]
        ordering = ["name"]


pre_save.connect(pre_save_slug, sender=Team, dispatch_uid="pre_save_team")
