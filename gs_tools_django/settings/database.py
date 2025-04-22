from .shared import env

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # Use PostgreSQL as the backend
        "NAME": env("GSTOOLS_POSTGRES_DB"),  # Database name
        "USER": env("GSTOOLS_POSTGRES_USER"),  # Username
        "PASSWORD": env("GSTOOLS_POSTGRES_PASSWORD"),  # Password
        "HOST": env("GSTOOLS_POSTGRES_HOST"),  # Database host IP
        "PORT": env("GSTOOLS_POSTGRES_PORT", default=5432),  # Port number
    }
}
