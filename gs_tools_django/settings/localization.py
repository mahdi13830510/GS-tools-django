from django.utils.translation import gettext_lazy as _

from .shared import BASE_DIR, env

USE_I18N = env.bool("GSTOOLS_USE_I18N", default=True)
USE_L10N = env.bool("GSTOOLS_USE_L10N", default=True)

LANGUAGE_CODE = env("GSTOOLS_LANGUAGE_CODE", default="en-us")
LANGUAGES = [
    ("en", _("English")),
    ("fa", _("Persian")),
]

LOCALE_PATHS = [
    BASE_DIR / "gs_tools_django" / "locale",
    BASE_DIR / "gs_tools_django" / "locale_extra" / "drf_simplejwt",
]

ALLOW_UNICODE_SLUGS = env.bool("GSTOOLS_ALLOW_UNICODE_SLUGS", default=True)

TIME_ZONE = env("GSTOOLS_TIMEZONE", default="UTC")
USE_TZ = env.bool("GSTOOLS_USE_TZ", default=True)

PHONENUMBER_DEFAULT_REGION = "IR"