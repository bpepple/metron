from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=25)
    desc = models.TextField("Description", blank=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
