from datetime import timedelta

from .shared import DEBUG, env

# Email
EMAIL_BACKEND = env("GSTOOLS_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_NOTIFICATIONS_ENABLED = env.bool("GSTOOLS_EMAIL_NOTIFICATIONS_ENABLED", default=False)
EMAIL_HOST = env("GSTOOLS_EMAIL_HOST", default=None)
EMAIL_PORT = env.int("GSTOOLS_EMAIL_PORT", default=465)
EMAIL_HOST_USER = env("GSTOOLS_EMAIL_HOST_USER", default=None)
EMAIL_HOST_PASSWORD = env("GSTOOLS_EMAIL_HOST_PASSWORD", default=None)
EMAIL_USE_TLS = env.bool("GSTOOLS_EMAIL_USE_TLS", default=False)
EMAIL_USE_SSL = env.bool("GSTOOLS_EMAIL_USE_SSL", default=True)
EMAIL_NOTIFICATION_RECIPIENTS = env.list("GSTOOLS_EMAIL_NOTIFICATION_RECIPIENTS", default=list())
EMAIL_NOTIFICATION_DEFAULT_FROM_EMAIL = env(
    "GSTOOLS_EMAIL_NOTIFICATION_DEFAULT_FROM_EMAIL",
    default=None,
)

if EMAIL_NOTIFICATIONS_ENABLED and (
    EMAIL_HOST is None
    or EMAIL_HOST_USER is None
    or EMAIL_HOST_PASSWORD is None
    or EMAIL_NOTIFICATION_DEFAULT_FROM_EMAIL is None
):
    msg = "You must set smtp host, user, password and default from email for email notifications."
    raise ValueError(msg)

# Token generation configuration
EMAIL_VERIFICATION_SECRET_KEY = (
    "debug__email__secret" if DEBUG else env("GSTOOLS_EMAIL_VERIFICATION_SECRET_KEY")
)
EMAIL_VERIFICATION_TOKEN_EXPIRY = timedelta(
    seconds=env.int("GSTOOLS_EMAIL_VERIFICATION_TOKEN_EXPIRY", 86400),
)
PASSWORD_VERIFICATION_SECRET_KEY = (
    "debug__password__secret" if DEBUG else env("GSTOOLS_PASSWORD_VERIFICATION_SECRET_KEY")
)
PASSWORD_RESET_TOKEN_EXPIRY = timedelta(
    seconds=env.int("GSTOOLS_PASSWORD_RESET_TOKEN_EXPIRY", 86400),
)
VERIFICATION_EMAIL_REQUEST_CACHE_TTL = env.int(
    "GSTOOLS_VERIFICATION_EMAIL_REQUEST_CACHE_TTL", 43200
)
PASSWORD_RESET_REQUEST_CACHE_TTL = env.int("GSTOOLS_PASSWORD_RESET_REQUEST_CACHE_TTL", 43200)

OTP_LENGTH = env.int("GSTOOLS_OPT_LENGTH", default=5)
OTP_LIFETIME_SECONDS = timedelta(seconds=env.int("GSTOOLS_OTP_LIFETIME_SECONDS", default=300))
OTP_REQUEST_TTL = env.int("GSTOOLS_OTP_REQUEST_TTL", 120)
