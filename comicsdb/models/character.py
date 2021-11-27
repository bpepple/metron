from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from simple_history.models import HistoricalRecords
from sorl.thumbnail import ImageField

from users.models import CustomUser

from .common import CommonInfo, pre_save_slug
from .creator import Creator
from .team import Team


class Character(CommonInfo):
    wikipedia = models.CharField("Wikipedia Slug", max_length=255, blank=True)
    image = ImageField(upload_to="character/%Y/%m/%d/", blank=True)
    alias = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    creators = models.ManyToManyField(Creator, blank=True)
    teams = models.ManyToManyField(Team, blank=True)
    edited_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)
    history = HistoricalRecords()

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

    def __str__(self) -> str:
        return self.name


pre_save.connect(pre_save_slug, sender=Character, dispatch_uid="pre_save_character")
