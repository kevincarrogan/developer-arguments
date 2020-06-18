from starlette.config import Config
from starlette.datastructures import URL

config = Config()

DEBUG = config("DEBUG", cast=bool, default=False)
SENTRY_URL = config("SENTRY_URL", cast=URL, default=None)
RELEASE = config("RELEASE", cast=str, default="local")
