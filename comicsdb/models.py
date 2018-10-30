from django.db import models
from django.urls import reverse


class Creator(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    desc = models.TextField('Description', blank=True)
    birth = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    founded = models.PositiveSmallIntegerField(null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)
    short_desc = models.CharField(max_length=350, blank=True)
    desc = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True)

    def get_absolute_url(self):
        return reverse('publisher:detail', args=[self.slug])

    @property
    def series_count(self):
        return self.series_set.all().count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Role(models.Model):
    name = models.CharField(max_length=25)
    notes = models.TextField(blank=True)

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
    volume = models.PositiveSmallIntegerField(null=True, blank=True)
    year_began = models.PositiveSmallIntegerField()
    year_end = models.PositiveSmallIntegerField(null=True, blank=True)
    series_type = models.ForeignKey(SeriesType, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    short_desc = models.CharField(max_length=350, blank=True)
    desc = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('series:detail', args=[self.slug])

    def __str__(self):
        return f'{self.name} ({self.year_began})'

    @property
    def issue_count(self):
        return self.issue_set.all().count()

    class Meta:
        verbose_name_plural = 'Series'
        ordering = ['sort_name', 'year_began']


class Issue(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    number = models.CharField(max_length=25)
    cover_date = models.DateField('Cover Date', null=True, blank=True)
    store_date = models.DateField('In Store Date', null=True, blank=True)
    desc = models.TextField('Description', blank=True)
    image = models.ImageField('Cover', upload_to='images/%Y/%m/%d/',
                              blank=True)
    creators = models.ManyToManyField(Creator, through='Credits', blank=True)

    def __str__(self):
        return f'{self.series.name} #{self.number}'

    class Meta:
        ordering = ['series__name', 'cover_date', 'number']


class Credits(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    role = models.ManyToManyField(Role)

    class Meta:
        verbose_name_plural = "Credits"
        unique_together = ['creator', 'issue']
        ordering = ['creator__name']
