from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from simple_history.models import HistoricalRecords
from sorl.thumbnail import ImageField

from users.models import CustomUser

from .common import CommonInfo, pre_save_slug
from .creator import Creator


class Team(CommonInfo):
    wikipedia = models.CharField("Wikipedia Slug", max_length=255, blank=True)
    image = ImageField(upload_to="team/%Y/%m/%d/", blank=True)
    creators = models.ManyToManyField(Creator, blank=True)
    edited_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse("team:detail", args=[self.slug])

    @property
    def issue_count(self):
        return self.issue_set.all().count()

    def __str__(self) -> str:
        return self.name


pre_save.connect(pre_save_slug, sender=Team, dispatch_uid="pre_save_team")
