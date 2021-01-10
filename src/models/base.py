from aiogram.utils.executor import Executor
from loguru import logger
from gino import Gino

from src.config import POSTGRES_URI

db_ = Gino()


async def on_startup(dp):
    bind = await db_.set_bind(POSTGRES_URI)

    await db_.gino.create_all(bind=bind)


async def on_shutdown(dp):
    bind = db_.pop_bind()
    if bind:
        logger.info("Closing Postgres Connection...")
        await bind.close()


def setup(executor: Executor):
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
