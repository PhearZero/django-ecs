from .settings import *

# TODO: Configure debug tools
INSTALLED_APPS = [
    # Developer Tools
    "django_browser_reload"
]

MIDDLEWARE = [
    # Developer Tools
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]
