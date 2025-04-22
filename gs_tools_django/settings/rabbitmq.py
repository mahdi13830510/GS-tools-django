from .shared import env

BROKER_URL = env("GSTOOLS_BROKER_URL", default="amqp://guest:guest@127.0.0.1:5672")
