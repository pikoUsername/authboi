from contextlib import suppress

from aiogram.utils.executor import Executor
from loguru import logger
from gino import Gino, UninitializedError, GinoEngine

from iternal.config import POSTGRES_URI

db_ = Gino()


async def get_pool(*args, **kwargs) -> GinoEngine:
    pool = await db_.set_bind(POSTGRES_URI, *args, **kwargs)
    return pool


async def on_startup(dp):
    bind = await get_pool()
    dp.bot['db_pool'] = bind
    logger.info("created Postgres Connection")
    await db_.gino.create_all(bind=bind)  # bind or pool nvm honestly


async def on_shutdown(dp):
    with suppress(UninitializedError):
        logger.info("Closing Postgres Connection...")
        await db_.pop_bind().close()


def setup(executor: Executor):
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
