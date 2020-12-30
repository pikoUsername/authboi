from typing import List

from aiogram import types
from loguru import logger
from gino.schema import GinoSchemaVisitor
from gino import Gino

from src.config import POSTGRES_URI

db_ = Gino()

async def create_db():
    await db_.set_bind(POSTGRES_URI)

    db_.gino: GinoSchemaVisitor
    await db_.gino.create_all()


async def close_db():
    bind = db_.pop_bind()
    if bind:
        logger.info("Closing DB...")
        await bind.close()
