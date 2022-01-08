from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from sorl.thumbnail import ImageField

from users.models import CustomUser

from .common import CommonInfo, pre_save_slug


class Arc(CommonInfo):
    image = ImageField(upload_to="arc/%Y/%m/%d/", blank=True)
    edited_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)

    @property
    def issue_count(self):
        return self.issue_set.all().count()

    def get_absolute_url(self):
        return reverse("arc:detail", args=[self.slug])

    def __str__(self) -> str:
        return self.name


pre_save.connect(pre_save_slug, sender=Arc, dispatch_uid="pre_save_arc")
