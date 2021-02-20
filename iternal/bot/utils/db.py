from contextlib import suppress

from aiogram.utils.executor import Executor
from gino import UninitializedError

from loguru import logger
from iternal.store.base import db_
from iternal.config import POSTGRES_URI

__all__ = "setup",


async def on_startup(dp):
    bind = await db_.set_bind(POSTGRES_URI)
    dp.bot['db_pool'] = bind
    logger.info("created Postgres Connection")
    await db_.gino.create_all(bind=bind)  # bind or pool nvm honestly


async def on_shutdown(_):
    with suppress(UninitializedError):
        logger.info("Closing Postgres Connection...")
        await db_.pop_bind().close()


def setup(executor: Executor):
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
