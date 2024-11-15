from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "p2vyxQTULwtjbI-FMYqH812eM9n70TBIpyjH3gv4r-8"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS = [
    'user',
]

AUTH = {
    "ACCESS": timedelta(days=100),
    "REFRESH": timedelta(minutes=10),
    "ALGORITHM": "HS256"
}

USER_MODEL = 'user.models:User'

ASGI = "TestFastTower.asgi:app"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_TZ = True

# Database
DATABASES = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {
                "file_path": str(BASE_DIR / "db.sqlite3"),
            }
        },
    },
}

# https://github.com/fastapi-admin/fastapi-admin
ADMIN_PANEL_REDIS = 'redis://localhost:6379/0'
