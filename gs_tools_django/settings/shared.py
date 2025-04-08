import pathlib

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

env = environ.Env()
env.read_env(BASE_DIR / ".env")

# WARN: don't run with debug turned on in production.
DEBUG = env.bool("GSTOOLS_DEBUG", default=False)