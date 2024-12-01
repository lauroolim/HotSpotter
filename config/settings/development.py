from .base import *
from decouple import config

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": "postgres",
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": "localhost",
        "PORT": "5432",
    }
}
