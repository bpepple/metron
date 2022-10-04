from django.db import models


class Rating(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
