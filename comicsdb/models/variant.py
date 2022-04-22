from django.db import models
from sorl.thumbnail import ImageField

from .issue import Issue


class Variant(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    image = ImageField("Variant Cover", upload_to="variants/%Y/%m/%d/")
    name = models.CharField("Name", max_length=255, blank=True)
    sku = models.CharField("Distributor SKU", max_length=9, blank=True)
    upc = models.CharField("UPC Code", max_length=20, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        indexes = [models.Index(fields=["issue"], name="issue_idx")]
        ordering = ["issue"]
