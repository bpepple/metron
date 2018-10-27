from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    founded = models.DateField(null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)
    short_desc = models.CharField(max_length=350, blank=True)
    desc = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True)

    @property
    def series_count(self):
        return self.series_set.all().count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class SeriesType(models.Model):
    name = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Series(models.Model):
    name = models.CharField(max_length=255)
    sort_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    volume = models.PositiveSmallIntegerField(null=True)
    year_began = models.PositiveSmallIntegerField(null=True)
    year_end = models.PositiveSmallIntegerField(null=True)
    type = models.ForeignKey(SeriesType, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    short_desc = models.CharField(max_length=350, blank=True)
    desc = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Series'
        ordering = ['sort_name', 'year_began']
