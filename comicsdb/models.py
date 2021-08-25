import itertools

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify
from simple_history.models import HistoricalRecords
from sorl.thumbnail import ImageField

from users.models import CustomUser


def generate_slug_from_name(instance):
    slug_candidate = slug_original = slugify(instance.name)
    Klass = instance.__class__
    for i in itertools.count(1):
        if not Klass.objects.filter(slug=slug_candidate).exists():
            break
        slug_candidate = f"{slug_original}-{i}"

    return slug_candidate


def pre_save_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = generate_slug_from_name(instance)


class Arc(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True)
    desc = models.TextField("Description", blank=True)
    image = ImageField(upload_to="arc/%Y/%m/%d/", blank=True)
    modified = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)
    history = HistoricalRecords()

    @property
    def issue_count(self):
        return self.issue_set.all().count()

    def get_absolute_url(self):
        return reverse("arc:detail", args=[self.slug])

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


pre_save.connect(pre_save_slug, sender=Arc, dispatch_uid="pre_save_arc")


class Creator(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True)
    desc = models.TextField("Description", blank=True)
    wikipedia = models.CharField("Wikipedia Slug", max_length=255, blank=True)
    birth = models.DateField("Date of Birth", null=True, blank=True)
    death = models.DateField("Date of Death", null=True, blank=True)
    image = ImageField(upload_to="creator/%Y/%m/%d/", blank=True)
    alias = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)
    history = HistoricalRecords()

    @property
    def issue_count(self):
        return self.credits_set.all().count()

    @property
    def recent_issues(self):
        return self.credits_set.order_by("-issue__cover_date").all()[:5]

    def get_absolute_url(self):
        return reverse("creator:detail", args=[self.slug])

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


pre_save.connect(pre_save_slug, sender=Creator, dispatch_uid="pre_save_creator")


class Team(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True)
    desc = models.TextField("Description", blank=True)
    wikipedia = models.CharField("Wikipedia Slug", max_length=255, blank=True)
    image = ImageField(upload_to="team/%Y/%m/%d/", blank=True)
    creators = models.ManyToManyField(Creator, blank=True)
    modified = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse("team:detail", args=[self.slug])

    @property
    def issue_count(self):
        return self.issue_set.all().count()

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


pre_save.connect(pre_save_slug, sender=Team, dispatch_uid="pre_save_team")


class Character(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True)
    desc = models.TextField("Description", blank=True)
    wikipedia = models.CharField("Wikipedia Slug", max_length=255, blank=True)
    image = ImageField(upload_to="character/%Y/%m/%d/", blank=True)
    alias = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    creators = models.ManyToManyField(Creator, blank=True)
    teams = models.ManyToManyField(Team, blank=True)
    modified = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
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

    class Meta:
        ordering = ["name"]


pre_save.connect(pre_save_slug, sender=Character, dispatch_uid="pre_save_character")


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    founded = models.PositiveSmallIntegerField("Year Founded", null=True, blank=True)
    desc = models.TextField("Description", blank=True)
    wikipedia = models.CharField("Wikipedia Slug", max_length=255, blank=True)
    image = ImageField("Logo", upload_to="publisher/%Y/%m/%d/", blank=True)
    modified = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse("publisher:detail", args=[self.slug])

    @property
    def series_count(self):
        return self.series_set.all().count()

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


pre_save.connect(pre_save_slug, sender=Publisher, dispatch_uid="pre_save_publisher")


class Role(models.Model):
    name = models.CharField(max_length=25)
    order = models.PositiveSmallIntegerField(unique=True)
    notes = models.TextField(blank=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["order"]


class SeriesType(models.Model):
    name = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class Series(models.Model):
    name = models.CharField(max_length=255)
    sort_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    volume = models.PositiveSmallIntegerField("Volume Number")
    year_began = models.PositiveSmallIntegerField("Year Began")
    year_end = models.PositiveSmallIntegerField("Year Ended", null=True, blank=True)
    series_type = models.ForeignKey(SeriesType, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    desc = models.TextField("Description", blank=True)
    modified = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse("series:detail", args=[self.slug])

    def __str__(self) -> str:
        return f"{self.name} ({self.year_began})"

    def first_issue_cover(self):
        try:
            return self.issue_set.all().first().image
        except AttributeError:
            return None

    @property
    def issue_count(self) -> int:
        return self.issue_set.all().count()

    class Meta:
        verbose_name_plural = "Series"
        unique_together = ["publisher", "name", "volume"]
        ordering = ["sort_name", "year_began"]


def generate_series_slug(instance):
    slug_candidate = slug_original = slugify(f"{instance.name}-{instance.year_began}")
    Klass = instance.__class__
    for i in itertools.count(1):
        if not Klass.objects.filter(slug=slug_candidate).exists():
            break
        slug_candidate = f"{slug_original}-{i}"

    return slug_candidate


def pre_save_series_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = generate_series_slug(instance)


pre_save.connect(pre_save_series_slug, sender=Series, dispatch_uid="pre_save_series")


class Issue(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    name = ArrayField(models.CharField("Story Title", max_length=150), null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    number = models.CharField(max_length=25)
    arcs = models.ManyToManyField(Arc, blank=True)
    cover_date = models.DateField("Cover Date")
    store_date = models.DateField("In Store Date", null=True, blank=True)
    price = models.DecimalField(
        "Cover Price", max_digits=5, decimal_places=2, null=True, blank=True
    )
    sku = models.CharField("Distributor SKU", max_length=9, blank=True)
    upc = models.CharField("UPC Code", max_length=14, blank=True)
    desc = models.TextField("Description", blank=True)
    image = ImageField("Cover", upload_to="issue/%Y/%m/%d/", blank=True)
    creators = models.ManyToManyField(Creator, through="Credits", blank=True)
    characters = models.ManyToManyField(Character, blank=True)
    teams = models.ManyToManyField(Team, blank=True)
    modified = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse("issue:detail", args=[self.slug])

    def __str__(self) -> str:
        return f"{self.series.name} #{self.number}"

    class Meta:
        unique_together = ["series", "number"]
        ordering = ["series__sort_name", "cover_date", "store_date", "number"]


def generate_issue_slug(issue):
    slug_candidate = slug_original = slugify(f"{issue.series.slug}-{issue.number}")
    for i in itertools.count(1):
        if not Issue.objects.filter(slug=slug_candidate).exists():
            break
        slug_candidate = f"{slug_original}-{i}"

    return slug_candidate


def pre_save_issue_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_issue_slug(instance)


pre_save.connect(pre_save_issue_slug, sender=Issue)


class Variant(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    image = ImageField("Variant Cover", upload_to="variants/%Y/%m/%d/")
    name = models.CharField("Name", max_length=255, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["issue"]


class Credits(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    role = models.ManyToManyField(Role)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Credits"
        unique_together = ["issue", "creator"]
        ordering = ["issue", "creator__name"]
