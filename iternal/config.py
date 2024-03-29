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


proj_path = Path(__name__).parent.parent
ON_STARTUP_NOTIFY = os.getenv("ON_STARTUP_NOTIFY", False)
# psql
POSTGRES_NAME = dstr("DB_NAME")
POSTGRES_HOST = dstr("DB_HOST")
POSTGRES_PORT = dint("DB_PORT")
POSTGRES_USER = dstr("DB_USER")
POSTGRES_PASS = dstr("DB_PASS")

# telegram
BOT_TOKEN = dstr("BOT_TOKEN")
ADMIN_IDS = [
    os.getenv("ADMIN_IDS"),
    935770891,
]
BOT_PUBLIC_PORT = dint("BOT_PUBLIC_PORT", default=3030)
# logs path
LOGS_BASE_PATH = str(proj_path / "logs")
POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"

DEBUG = True

# webhook
DOMAIN = os.getenv("DOMAIN", default="localhost")
WEBHOOK_BASE_PATH = str(os.getenv("WEBHOOK_BASE_PATH", default="/webhook"))
WEBHOOK_PATH = f"{WEBHOOK_BASE_PATH}/{BOT_TOKEN}"
WEBHOOK_URL = f"https://{DOMAIN}{WEBHOOK_PATH}"
