from datetime import timedelta

from .shared import env

APPEND_SLASH = True
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework_simplejwt.authentication.JWTAuthentication"],
    "PAGE_SIZE": env.int("SAMAP_REST_PAGE_SIZE", default=25),
}


ACCESS_TOKEN_LIFETIME_SECONDS = env.int(
    "GSTOOLS_ACCESS_TOKEN_LIFETIME_SECONDS",
    default=3600,
)
REFRESH_TOKEN_LIFETIME_SECONDS = env.int(
    "GSTOOLS_REFRESH_TOKEN_LIFETIME_SECONDS",
    default=86400,
)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=ACCESS_TOKEN_LIFETIME_SECONDS),
    "REFRESH_TOKEN_LIFETIME": timedelta(seconds=REFRESH_TOKEN_LIFETIME_SECONDS),
}