import contextlib
import itertools
import logging

import imagehash
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image
from sorl.thumbnail import ImageField

from users.models import CustomUser

from .arc import Arc
from .attribution import Attribution
from .character import Character
from .common import CommonInfo
from .creator import Creator
from .rating import Rating
from .series import Series
from .team import Team

LOGGER = logging.getLogger(__name__)


class GraphicNovelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(series__series_type__name="Graphic Novel")


class TradePaperbackManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(series__series_type__name="Trade Paperback")


class Issue(CommonInfo):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    name = ArrayField(models.CharField("Story Title", max_length=150), null=True, blank=True)
    title = models.CharField("Collection Title", max_length=255, blank=True)
    number = models.CharField(max_length=25)
    cover_date = models.DateField("Cover Date")
    store_date = models.DateField("In Store Date", null=True, blank=True)
    price = models.DecimalField(
        "Cover Price", max_digits=5, decimal_places=2, null=True, blank=True
    )
    rating = models.ForeignKey(Rating, default=1, on_delete=models.SET_DEFAULT)
    sku = models.CharField("Distributor SKU", max_length=9, blank=True)
    isbn = models.CharField("ISBN", max_length=13, blank=True)
    upc = models.CharField("UPC Code", max_length=20, blank=True)
    page = models.PositiveSmallIntegerField("Page Count", null=True, blank=True)
    image = ImageField("Cover", upload_to="issue/%Y/%m/%d/", blank=True)
    cover_hash = models.CharField("Cover Hash", max_length=25, blank=True)
    arcs = models.ManyToManyField(Arc, blank=True)
    creators = models.ManyToManyField(Creator, through="Credits", blank=True)
    characters = models.ManyToManyField(Character, blank=True)
    teams = models.ManyToManyField(Team, blank=True)
    reprints = models.ManyToManyField("self", blank=True)
    attribution = GenericRelation(Attribution, related_query_name="issues")
    created_by = models.ForeignKey(CustomUser, default=1, on_delete=models.SET_DEFAULT)
    edited_by = models.ForeignKey(
        CustomUser, default=1, on_delete=models.SET_DEFAULT, related_name="editor"
    )

    objects = models.Manager()
    graphic_novels = GraphicNovelManager()
    tpb = TradePaperbackManager()

    def get_absolute_url(self):
        return reverse("issue:detail", args=[self.slug])

    @property
    def wikipedia(self):
        return self.attribution.filter(source=Attribution.Source.WIKIPEDIA)

    @property
    def marvel(self):
        return self.attribution.filter(source=Attribution.Source.MARVEL)

    def save(self, *args, **kwargs) -> None:
        # Let's delete the original image if we're replacing it by uploading a new one.
        with contextlib.suppress(ObjectDoesNotExist):
            this: Issue = Issue.objects.get(id=self.id)
            if this.image and this.image != self.image:
                LOGGER.info(
                    f"Replacing {this.image} with {img if (img:=self.image) else 'None'}."
                )

                this.image.delete(save=False)
        return super(Issue, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.series} #{self.number}"

    class Meta:
        indexes = [
            models.Index(
                fields=["series", "cover_date", "store_date", "number"],
                name="series_cover_store_num_idx",
            ),
            models.Index(fields=["series", "number"], name="series_number_idx"),
        ]
        ordering = ["series__sort_name", "cover_date", "store_date", "number"]
        unique_together = ["series", "number"]


def generate_issue_slug(instance: Issue):
    slug_candidate = slug_original = slugify(f"{instance.series.slug}-{instance.number}")
    for i in itertools.count(1):
        if not Issue.objects.filter(slug=slug_candidate).exists():
            break
        slug_candidate = f"{slug_original}-{i}"

    return slug_candidate


def pre_save_issue_slug(sender, instance: Issue, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_issue_slug(instance)


def generate_cover_hash(instance: Issue) -> str:
    try:
        cover_hash = imagehash.phash(Image.open(instance.image))
    except OSError as e:
        LOGGER.error(f"Unable to generate cover hash for '{instance}': {e}")
        return ""
    return str(cover_hash)


def pre_save_cover_hash(sender, instance: Issue, *args, **kwargs):
    if instance.image and not instance.cover_hash:
        instance.cover_hash = generate_cover_hash(instance)
        LOGGER.info(f"Adding cover hash: '{instance.cover_hash}' to '{instance}'")

    if not instance.image and instance.cover_hash:
        LOGGER.info(f"Removing old cover hash: '{instance.cover_hash}' from '{instance}'")
        instance.cover_hash = ""


pre_save.connect(pre_save_issue_slug, sender=Issue)
pre_save.connect(pre_save_cover_hash, sender=Issue)
