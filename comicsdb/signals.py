import logging

from sorl.thumbnail import delete

LOGGER = logging.getLogger(__name__)


def pre_delete_image(sender, instance, **kwargs):
    if instance.image:
        delete(instance.image)


def pre_delete_credit(sender, instance, **kwargs):
    LOGGER.info(f"Deleting {instance.creator} credit for {instance.issue}")
