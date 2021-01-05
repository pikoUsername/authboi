import os
from typing import Optional
import secrets

from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def dstr(key: str, default: Optional[str] = None):
    return str(os.getenv(key, default))


def dint(key: str, default: Optional[int] = 0):
    return os.getenv(key, default)


ON_STARTUP_NOTIFY = os.getenv("ON_STARTUP_NOTIFY", False)
# psql
POSTGRES_NAME = dstr("DB_NAME")
POSTGRES_HOST = dstr("DB_HOST")
POSTGRES_PORT = dint("DB_PORT")
POSTGRES_USER = dstr("DB_USER")
POSTGRES_PASS = dstr("DB_PASS")


# webhook
DOMAIN = dstr("DOMAIN", default="localhost")
SECRET_KEY = secrets.token_urlsafe(48)
WEBHOOK_BASE_PATH = dstr("WEBHOOK_BASE_PATH", default="/webhook")
WEBHOOK_PATH = f"{WEBHOOK_BASE_PATH}/{SECRET_KEY}"
WEBHOOK_URL = f"https://{DOMAIN}{WEBHOOK_PATH}"


# telegram
BOT_TOKEN = dstr("BOT_TOKEN")
ADMIN_IDS = [
    os.getenv("ADMIN_IDS"),
    935770891,
]
BOT_PUBLIC_PORT = dint("BOT_PUBLIC_PORT", default=8080)
# logs path
LOGS_BASE_PATH = str(Path(__name__).parent.parent / "logs")
POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"