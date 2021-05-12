from django.contrib.auth.models import AbstractUser
from django.db import models
from sorl.thumbnail import ImageField


class CustomUser(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    image = ImageField(upload_to="user/", blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
