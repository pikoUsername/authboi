import datetime
from typing import List

from sqlalchemy import sql
import sqlalchemy as sa

from .util import ContextGino


__all__ = "db_",

# please don't make duplicates of this object
# it s can be dangerous
db_ = ContextGino()  # for backward compatibility
# this var uses by handlers and etc.
# if indeed need to copy this object, so just delete in end of file


class BaseModel(db_.Model):
    __abstract__ = 1
    query: sql.Select

    id = db_.Column(db_.Integer(), index=True, primary_key=True, unique=True)

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
    __abstract__ = 1

    created_at = db_.Column(db_.DateTime(True), server_default=db.func.now())
    updated_at = db_.Column(
        db_.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=db_.func.now(),
    )
