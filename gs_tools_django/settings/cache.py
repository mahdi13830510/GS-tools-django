from .shared import env

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("GSTOOLS_CACHING_HOST_LOCATION"),
    },
}

## cacheops

CACHEOPS_REDIS = {
    "host": env.str("GSTOOLS_CACHEOPS_REDIS_HOST", default="127.0.0.1"),
    "port": env.int("GSTOOLS_CACHEOPS_REDIS_PORT", default=6379),
    "db": env.int("GSTOOLS_CACHEOPS_REDIS_DB_NUMBER", default=1),
    "socket_timeout": env.int("GSTOOLS_CACHEOPS_REDIS_SOCKET_TIMEOUT_SECONDS", default=3),
    "password": env.str("GSTOOLS_CACHEOPS_REDIS_PASSWORD", default=None),
    "unix_socket_path": env.str("GSTOOLS_CACHEOPS_REDIS_UNIX_SOCKET_PATH", default=None),
}
