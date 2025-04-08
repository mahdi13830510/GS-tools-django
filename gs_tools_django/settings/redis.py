from .shared import env

REDIS_URL = env("GSTOOLS_REDIS_URL", default="redis://127.0.0.1:6379")