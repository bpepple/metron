from django.contrib.auth.models import AbstractUser
from django.db import models
from sorl.thumbnail import ImageField


class CustomUser(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    image = ImageField(upload_to="user/", blank=True)

    def __str__(self):
        return self.username
