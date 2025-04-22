from collections.abc import Sequence
from enum import StrEnum

from django.core.exceptions import ImproperlyConfigured

from .shared import env


class SmsProvider(StrEnum):
    KAVENEGAR = "kavenegar"


# WARN: keep the secret key used in production secret.
SECRET_KEY = env.str("GSTOOLS_SECRET_KEY", default=None)

ALLOWED_HOSTS = env.list("GSTOOLS_ALLOWED_HOSTS", default=["127.0.0.1", "0.0.0.0"])  # noqa S104

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

KAVENEGAR_API_TEMPLATE_LOGIN_VERIFICATION = env.str(
    "GSTOOLS_KAVENEGAR_API_TEMPLATE_LOGIN_VERIFICATION",
    default="gs_tools_django-login-code",
)

SMS_NOTIFICATION_IS_ENABLED = env.bool("GSTOOLS_SMS_NOTIFICATIONS_IS_ENABLED", default=False)

ALLOWED_SMS_PROVIDERS = [SmsProvider.KAVENEGAR]
SMS_PROVIDER = env.str("GSTOOLS_SMS_PROVIDER", default=SmsProvider.KAVENEGAR)

KAVENEGAR_API_KEY = env.str("GSTOOLS_KAVENEGAR_API_KEY", default="")

## Cors
CORS_ALLOW_ALL_ORIGINS = env.bool("GSTOOLS_CORS_ALLOW_ALL_ORIGINS", default=True)
CORS_ALLOWED_ORIGINS: Sequence[str] = env.list(
    "GSTOOLS_CORS_ALLOWED_ORIGINS", default=["https://gs-tools.kubarcloud.net"]
)
CORS_DEFAULT_ALLOW_HEADERS = env.list(
    "GSTOOLS_CORS_DEFAULT_ALLOW_HEADERS",
    default=[
        "accept",
        "authorization",
        "content-type",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
    ],
)
CORS_EXTRA_ALLOW_HEADERS = env.list(
    "GSTOOLS_CORS_EXTRA_ALLOW_HEADERS",
    default=[
        "accept",
        "authorization",
        "content-type",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
    ],
)
CORS_ALLOW_HEADERS = env.list(
    "GSTOOLS_CORS_ALLOW_HEADERS", default=CORS_DEFAULT_ALLOW_HEADERS + CORS_EXTRA_ALLOW_HEADERS
)

## CSRF
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS: Sequence[str] = env.list("GSTOOLS_CSRF_TRUSTED_ORIGINS", default=[])

if not SECRET_KEY:
    msg = "You should set the 'GSTOOLS_SECRET_KEY' env var and keep it secret."
    raise ImproperlyConfigured(msg)


if SMS_NOTIFICATION_IS_ENABLED:
    if SMS_PROVIDER not in ALLOWED_SMS_PROVIDERS:
        allowed_values: str = ", ".join(ALLOWED_SMS_PROVIDERS)
        error_msg = f"Provide a valid SMS provider. Allowed values are: {allowed_values}"
        raise ImproperlyConfigured(error_msg)

    if SMS_PROVIDER == SmsProvider.KAVENEGAR:
        if not KAVENEGAR_API_KEY:
            error_msg = (
                "You have to set a valid API key for Kavenegar using KAVENEGAR_API_KEY env var."
            )
            raise ImproperlyConfigured(error_msg)
