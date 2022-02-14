from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Attribution(models.Model):
    class Source(models.TextChoices):
        MARVEL = "M", "Marvel"
        WIKIPEDIA = "W", "Wikipedia"

    source = models.CharField(max_length=1, choices=Source.choices, default=Source.WIKIPEDIA)
    url = models.URLField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        unique_together = ["source", "content_type", "object_id"]
        ordering = ["content_type", "object_id"]
