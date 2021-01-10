from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiograph import Telegraph
from loguru import logger

from src import config
from src.models.api import DBCommands

db = DBCommands()
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
telegraph = Telegraph()


def setup():
    from . import middlewares, filters
    from .utils import executor

    executor.setup()
    middlewares.setup(dp)
    filters.setup(dp)

    logger.info("Configure Handlers")
    from . import handlers