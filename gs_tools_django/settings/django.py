from enum import StrEnum

from .shared import BASE_DIR, DEBUG, env


class FileUploadStrategy(StrEnum):
    S3 = "s3"
    LOCAL = "local"


ALLOWED_FILE_UPLOAD_STRATEGIES = [upload_strategy for upload_strategy in FileUploadStrategy]

WSGI_APPLICATION = env("GSTOOLS_WSGI_APPLICATION", default="gs_tools_django.wsgi.application")
ASGI_APPLICATION = env("GSTOOLS_ASGI_APPLICATION", default="gs_tools_django.asgi.application")

DJANGO_APPS_PREREQUISITS = []

DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    "health_check.contrib.celery",
    "health_check.contrib.celery_ping",
    "health_check.contrib.rabbitmq",
    "health_check.contrib.redis",
    "debug_toolbar",
    "django_filters",
    "phonenumber_field",
    "corsheaders",
    "cacheops",
    "silk",
]

LOCAL_APPS = [
    "gs_tools_django.core",
    "gs_tools_django.users",
    "gs_tools_django.authentication",
    "gs_tools_django.profiles",
    "gs_tools_django.products",
    "gs_tools_django.files",
]

DEBUG_APPS = []

EXTRA_APPS = env.list("GSTOOLS_EXTRA_APPS", default=[])

INSTALLED_APPS = DJANGO_APPS_PREREQUISITS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + EXTRA_APPS

if DEBUG:
    INSTALLED_APPS += DEBUG_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "gs_tools_django.core.middlewares.CustomLocaleMiddleware",
    # "gs_tools_django.core.middlewares.ExceptionMiddleware",
    "gs_tools_django.core.middlewares.AppendSlashMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "silk.middleware.SilkyMiddleware",
]

if DEBUG:
    # include the Debug Toolbar middleware as early as possible in the list.
    # However, it must come after any other middleware that encodes the
    # response`s content, such as GZipMiddleware
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")


# this is required by django-debug-toolbar because with every requests it only
# shows the toolbar if the request is coming from an internal ip in order to
# prevent security issues like SQL injection
DEFAULT_INTERNAL_IPS = ["127.0.0.1"]

if DEBUG:
    import socket

    # WARN: do not use `_` as variable name because it will be confused with gettext_lazy.
    hostname, __, ips = socket.gethostbyname_ex(socket.gethostname())
    DEFAULT_INTERNAL_IPS.extend([ip[: ip.rfind(".")] + ".1" for ip in ips] + ["10.0.2.2"])

EXTRA_INTERNAL_IPS = env.list(var="GSTOOLS_EXTRA_INTERNAL_IPS", cast=str, default=list())
INTERNAL_IPS = (
    env.list(var="GSTOOLS_INTERNAL_IPS", cast=str, default=DEFAULT_INTERNAL_IPS)
    + EXTRA_INTERNAL_IPS
)

APPEND_SLASH = env.bool("GSTOOLS_APPEND_SLASH", default=True)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ROOT_URLCONF = "gs_tools_django.urls"

STATIC_URL = env("GSTOOLS_STATIC_URL", default="static/")
STATIC_ROOT = BASE_DIR / env("GSTOOLS_STATIC_ROOT", default="static")

MEDIA_URL = env("GSTOOLS_MEDIA_URL", default="media/")
MEDIA_ROOT = BASE_DIR / env("GSTOOLS_MEDIA_ROOT", default="media")

## Files and S3
FILE_UPLOAD_STRATEGY = env.str("GSTOOLS_FILE_UPLOAD_STRATEGY", default=FileUploadStrategy.LOCAL)

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
DEFAULT_FILE_STORAGE = "gs_tools_django.core.storages.OverwriteStorage"

AWS_S3_ENDPOINT_URL = env.str("GSTOOLS_S3_ENDPOINT_URL", default="")
AWS_S3_ACCESS_KEY_ID = env.str("GSTOOLS_S3_ACCESS_KEY", default="")
AWS_S3_SECRET_ACCESS_KEY = env.str("GSTOOLS_S3_SECRET_KEY", default="")
AWS_STORAGE_BUCKET_NAME = env.str("GSTOOLS_S3_BUCKET_NAME", default="")

AWS_S3_MAX_MEMORY_SIZE = env.int("GSTOOLS_S3_MAX_MEMORY_SIZE", default=5242880)
AWS_QUERYSTRING_EXPIRE = env.int("GSTOOLS_S3_QUERYSTRING_EXPIRE", default=3600)


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_ALLOWED_IMAGE_EXTENSIONS = ["bmp", "jpeg", "jpg", "mpo", "png", "tif", "tiff", "webp"]

EXTRA_ALLOWED_IMAGE_EXTENSIONS = env.list("GSTOOLS_EXTRA_ALLOWED_IMAGE_EXTENSIONS", default=[])

ALLOWED_IMAGE_EXTENSIONS = env.list(
    "GSTOOLS_ALLOWED_IMAGE_EXTENSIONS",
    default=DEFAULT_ALLOWED_IMAGE_EXTENSIONS + EXTRA_ALLOWED_IMAGE_EXTENSIONS,
)

DEFAULT_ALLOWED_FILE_EXTENSIONS = ["pdf", "zip", "rar", "mp3", "ogg", "wav", "mp4"]

EXTRA_ALLOWED_FILE_EXTENSIONS = env.list("GSTOOLS_EXTRA_ALLOWED_FILE_EXTENSIONS", default=[])

ALLOWED_FILE_EXTENSIONS = env.list(
    "GSTOOLS_ALLOWED_FILE_EXTENSIONS",
    default=DEFAULT_ALLOWED_FILE_EXTENSIONS
    + EXTRA_ALLOWED_FILE_EXTENSIONS
    + ALLOWED_IMAGE_EXTENSIONS,
)

ALLOWED_UPLOADED_FILE_SIZE = env.int("GSTOOLS_ALLOWED_UPLOADED_FILE_SIZE", 1)  # In megabytes

AUTH_USER_MODEL = "users.User"
DEBUG_TOOLBAR_CONFIG = {
    "IS_RUNNING_TESTS": env.bool("DEBUG_TOOLBAR_IS_RUNNING_TESTS", default=False),
}
