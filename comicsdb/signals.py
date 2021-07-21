import itertools

from django.utils.text import slugify
from sorl.thumbnail import delete


def generate_slug_from_name(instance):
    slug_candidate = slug_original = slugify(instance.name)
    Klass = instance.__class__
    for i in itertools.count(1):
        if not Klass.objects.filter(slug=slug_candidate).exists():
            break
        slug_candidate = f"{slug_original}-{i}"

    return slug_candidate


def generate_series_slug(instance):
    slug_candidate = slug_original = slugify(f"{instance.name}-{instance.year_began}")
    Klass = instance.__class__
    for i in itertools.count(1):
        if not Klass.objects.filter(slug=slug_candidate).exists():
            break
        slug_candidate = f"{slug_original}-{i}"

    return slug_candidate


def pre_delete_image(sender, instance, **kwargs):
    if instance.image:
        delete(instance.image)


def pre_save_slug_from_name(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = generate_slug_from_name(instance)


def pre_save_series_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = generate_series_slug(instance)
