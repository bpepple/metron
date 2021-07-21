import itertools

from django.utils.text import slugify
from sorl.thumbnail import delete


def generate_slug_from_name(instance):
    slug_candidate = slug_original = slugify(instance.name, allow_unicode=True)
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
