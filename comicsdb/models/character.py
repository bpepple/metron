import contextlib
import logging

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from sorl.thumbnail import ImageField

from users.models import CustomUser

from .attribution import Attribution
from .common import CommonInfo, pre_save_slug
from .creator import Creator
from .team import Team

LOGGER = logging.getLogger(__name__)


class Character(CommonInfo):
    image = ImageField(upload_to="character/%Y/%m/%d/", blank=True)
    alias = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    creators = models.ManyToManyField(Creator, blank=True)
    teams = models.ManyToManyField(Team, blank=True)
    attribution = GenericRelation(Attribution, related_query_name="characters")
    edited_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)

    def save(self, *args, **kwargs) -> None:
        # Let's delete the original image if we're replacing it by uploading a new one.
        with contextlib.suppress(ObjectDoesNotExist):
            this = Character.objects.get(id=self.id)
            if this.image and this.image != self.image:
                LOGGER.info(
                    f"Replacing {this.image} with {img if (img:=self.image) else 'None'}."
                )

                this.image.delete(save=False)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("character:detail", args=[self.slug])

    @property
    def issue_count(self):
        return self.issue_set.all().count()

    @property
    def first_appearance(self):
        return self.issue_set.order_by("cover_date").all().first

    @property
    def recent_appearances(self):
        return self.issue_set.order_by("-cover_date").all()[:5]

    @property
    def wikipedia(self):
        return self.attribution.filter(source=Attribution.Source.WIKIPEDIA)

    @property
    def marvel(self):
        return self.attribution.filter(source=Attribution.Source.MARVEL)

    def __str__(self) -> str:
        return self.name

    class Meta:
        indexes = [models.Index(fields=["name"], name="character_name_idx")]
        ordering = ["name"]


pre_save.connect(pre_save_slug, sender=Character, dispatch_uid="pre_save_character")
