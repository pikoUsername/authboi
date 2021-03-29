from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiograph import Telegraph
from loguru import logger

from iternal import config
from iternal.store.api import DBCommands
# from iternal.bot.utils.help import HelpCommandEmbed

__all__ = (
    "db",
    "bot",
    "dp",
    "setup"
)

db = DBCommands()
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# expermintal
# help = HelpCommandEmbed(dp)
# # Can increase a runtime
# help.setup_handlers_to_telegram()
# help.setup()
telegraph = Telegraph()


# noinspection PyUnusedLocal
def setup():
    from . import middlewares, filters
    from .utils import executor

    executor.setup()
    middlewares.setup(dp)
    filters.setup(dp)

    logger.info("Configure Handlers...")
    from iternal.bot import handlers
