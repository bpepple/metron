"""
Django settings for metron project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import logging.config
from os import environ
from pathlib import Path

import chartkick
from decouple import Csv, config
from django.utils.log import DEFAULT_LOGGING

# Disable Django's logging setup
LOGGING_CONFIG = None

LOGLEVEL = environ.get("LOGLEVEL", "info").upper()

# Pushover Config
PUSHOVER_TOKEN = config("PUSHOVER_TOKEN")
PUSHOVER_USER_KEY = config("PUSHOVER_USER_KEY")

# Marvel API Keys
MARVEL_PUBLIC_KEY = config("MARVEL_PUBLIC_KEY")
MARVEL_PRIVATE_KEY = config("MARVEL_PRIVATE_KEY")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parents[1]

DEBUG = config("DEBUG", default=False, cast=bool)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# Application definition

INSTALLED_APPS = [
    "dal",
    "dal_select2",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.postgres",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.flatpages",
    "django.contrib.humanize",
    "django.forms",
    "rest_framework",
    "drf_spectacular",
    "django_filters",
    "widget_tweaks",
    "sorl.thumbnail",
    "django_simple_bulma",
    "chartkick",
    "simple_history",
    "comicsdb",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "metron.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "metron.wsgi.application"

# Custom User Model
AUTH_USER_MODEL = "users.CustomUser"

# Needed to override form widgets template
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# Site app id
SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST", ""),
        "PORT": "",
    }
}

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Define model primary keys
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# sorl-thumbnail settings
THUMBNAIL_KVSTORE = "sorl.thumbnail.kvstores.redis_kvstore.KVStore"
THUMBNAIL_REDIS_HOST = "localhost"  # default
THUMBNAIL_REDIS_PORT = 6379  # default

# REST settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_THROTTLE_CLASSES": ("rest_framework.throttling.UserRateThrottle",),
    "DEFAULT_THROTTLE_RATES": {"user": "25/minute"},
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 28,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Logging settings
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
            "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
        },
        "handlers": {
            # console logs to stderr
            "console": {"class": "logging.StreamHandler", "formatter": "default"},
            "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
        },
        "loggers": {
            # default for all undefined Python modules
            "": {"level": "WARNING", "handlers": ["console"]},
            # Our application code
            "comicsdb": {
                "level": LOGLEVEL,
                "handlers": ["console"],
                # Avoid double logging because of root logger
                "propagate": False,
            },
            "users": {
                "level": LOGLEVEL,
                "handlers": ["console"],
                # Avoid double logging because of root logger
                "propagate": False,
            },
            # Default runserver request logging
            "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
        },
    }
)


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "US/Eastern"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# E-mail settings
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# drf-spectacular settings
SPECTACULAR_SETTINGS = {
    "SERVE_PUBLIC": False,
    "TITLE": "Metron Comicbook Database",
    "DESCRIPTION": "API to retrieve comic book data",
    "CONTACT": {"name": "API Support", "email": EMAIL_HOST_USER},
    "VERSION": "1.0.0",
    "LICENSE": {
        "name": "Creative Commons License",
        "url": "https://creativecommons.org/licenses/by-sa/4.0/",
    },
}


STATICFILES_FINDERS = [
    # First add the two default Finders, since this will overwrite the default.
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # Now add our custom SimpleBulma one.
    "django_simple_bulma.finders.SimpleBulmaFinder",
]

# Custom settings for django-simple-bulma
BULMA_SETTINGS = {
    "extensions": [
        "bulma-calendar",
        "bulma-fileupload",
        "bulma-navbar-burger",
        "bulma-modal",
    ],
    "variables": {"navbar-height": "4.75rem", "footer-padding": "1rem 1.5rem 1rem"},
    "output_style": "compressed",
}

HCAPTCHA_SECRET_KEY = config("HCAPTCHA_SECRET_KEY")

if not DEBUG:
    # Production Security
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 15778800
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.1/howto/static-files/

    AWS_ACCESS_KEY_ID = config("DO_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("DO_SECRET_ACCESS_KEY")

    AWS_STORAGE_BUCKET_NAME = config("DO_STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = config("DO_S3_ENDPOINT_URL")
    AWS_S3_CUSTOM_DOMAIN = config("DO_S3_CUSTOM_DOMAIN")
    # Set the cache to 7 days. 86400 seconds/day * 7
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=604800",
        "ACL": "public-read",
    }
    AWS_LOCATION = "static"

    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    STATICFILES_DIRS = (chartkick.js(), BASE_DIR / "static")
    STATIC_URL = f"{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"

    DEFAULT_FILE_STORAGE = "metron.storage_backends.MediaStorage"
else:
    STATICFILES_DIRS = (chartkick.js(), BASE_DIR / "static")
    STATIC_URL = "/static/"
    STATIC_ROOT = config("STATIC_ROOT")

    MEDIA_URL = "/media/"
    MEDIA_ROOT = config("MEDIA_ROOT")
    INTERNAL_IPS = ("127.0.0.1", "localhost")
    MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

    INSTALLED_APPS += ("debug_toolbar",)

    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ]

    DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}
