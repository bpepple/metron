import chartkick
from decouple import config

from metron.settings.common import *

DEBUG = False

ALLOWED_HOSTS = ["metron.cloud", "127.0.0.1"]

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# E-mail settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
EMAIL_USE_TLS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

AWS_ACCESS_KEY_ID = config("DO_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("DO_SECRET_ACCESS_KEY")

AWS_STORAGE_BUCKET_NAME = config("DO_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = config("DO_S3_ENDPOINT_URL")
AWS_S3_CUSTOM_DOMAIN = config("DO_S3_CUSTOM_DOMAIN")
# Set the cache to 7 days. 86400 seconds/day * 7
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=604800"}
AWS_LOCATION = "static"
AWS_DEFAULT_ACL = "public-read"

STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

STATICFILES_DIRS = (chartkick.js(), os.path.join(BASE_DIR, "static"))
STATIC_URL = f"{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
STATIC_ROOT = config("STATIC_ROOT")

DEFAULT_FILE_STORAGE = "metron.settings.storage_backends.MediaStorage"
