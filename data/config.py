
import secrets

from envparse import env

# psql
POSTGRES_NAME = env.str("DB_NAME")
POSTGRES_HOST = env.str("DB_HOST")
POSTGRES_PORT = env.int("DB_PORT")
POSTGRES_USER = env.str("DB_USER")
POSTGRES_PASS = env.str("DB_PASS")

# webhook configs
DOMAIN = env.str("DOMAIN", default="localhost")
SECRET_KEY = secrets.token_urlsafe(48)
WEBHOOK_BASE_PATH = env.str("WEBHOOK_BASE_PATH", default="/webhook")
WEBHOOK_PATH = f"{WEBHOOK_BASE_PATH}:{SECRET_KEY}"
WEBHOOK_URL = f"https://{DOMAIN}{WEBHOOK_PATH}"

BOT_TOKEN = env.str("BOT_TOKEN")
ADMIN_IDS = [
    env.int("ADMIN_IDS")
]
TELEGRAM_PORT = env.int("TELEGRAM_PORT", default=5000)


POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"