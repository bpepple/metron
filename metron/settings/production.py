from decouple import config

from metron.settings.common import *

DEBUG = False

ALLOWED_HOSTS = ["metron.cloud", "127.0.0.1"]

# E-mail settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
EMAIL_USE_TLS = True
