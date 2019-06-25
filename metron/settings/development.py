import chartkick

from metron.settings.common import *

DEBUG = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = (chartkick.js(), os.path.join(BASE_DIR, "static"))

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Debug Settings
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
