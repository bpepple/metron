from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Attribution(models.Model):
    class Source(models.TextChoices):
        MARVEL = "M", "Marvel"
        WIKIPEDIA = "W", "Wikipedia"
        GCD = "G", "Grand Comics Database"
        DC = "D", "DC"

    source = models.CharField(max_length=1, choices=Source.choices, default=Source.WIKIPEDIA)
    url = models.URLField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        indexes = [models.Index(fields=["content_type", "object_id"], name="ct_obj_id_idx")]
        ordering = ["content_type", "object_id"]

    def __str__(self) -> str:
        return f"{self.source} Attribution"
