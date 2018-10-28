from django.apps import AppConfig
from django.db.models.signals import pre_delete

from comicsdb.signals import pre_delete_image


class ComicsdbConfig(AppConfig):
    name = 'comicsdb'

    def ready(self):
        publisher = self.get_model('Publisher')
        pre_delete.connect(pre_delete_image, sender=publisher,
                           dispatch_uid='pre_delete_publisher')
