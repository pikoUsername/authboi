import datetime
from typing import List

from sqlalchemy import sql
import sqlalchemy as sa
from loguru import logger

from ..config import POSTGRES_URI
from .util import ContextGino


__all__ = "db_", "setup"

# please don't make duplicates of this object
# it s can be dangerous
db_ = ContextGino()  # for backward compatibility
# this var uses by handlers and etc.
# if indeed need to copy this object, so just delete in end of file


class BaseModel(db_.Model):
    __abstract__ = True
    query: sql.Select

    id = db_.Column(db_.Integer(), db_.Sequence("users_id_seq"), index=True, primary_key=True)

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db_.Column(db_.DateTime(True), server_default=db_.func.now())
    updated_at = db_.Column(
        db_.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=db_.func.now(),
    )

async def on_startup(dispatcher):
    logger.info("Setup PostgreSQL Connection")
    await db_.set_bind(POSTGRES_URI)
    await db_.gino.create_all()


async def on_shutdown(dispatcher):
    bind = db_.pop_bind()
    if bind:
        logger.info("Close PostgreSQL Connection")
        await bind.close()


def setup(executor):
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
