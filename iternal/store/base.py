import datetime
from contextvars import ContextVar
from typing import Type, TypeVar, List

from sqlalchemy import sql
import sqlalchemy as sa
from gino import Gino


__all__ = "ContextGino", "db_"

T = TypeVar("T")


class ContextGino(Gino):
    """
    For context bind, and pool.
    usage is simple
    just ContextGino.get_current()  but only in functions, and something lke this
    and you should ready for atack of gino engine instance
    but take care about global "GINO"'s
    like that globals may raise huge problems
    """
    # unfortunetly, variant of
    # using with ContextInstanceMixin from aiogram
    # not working
    __context_instance = ContextVar("context_gino")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_current(ContextGino)

    @classmethod
    def get_current(cls: Type[T], no_error: bool = True) -> T:
        try:
            ctx = cls.__context_instance.get()
        except LookupError:
            if no_error:
                return
            raise
        else:
            return ctx

    @classmethod
    def set_current(cls: Type[T], value: T) -> None:
        assert not isinstance(value, cls), \
            f'Value should be instance of {cls.__name__!r} not {type(value).__name__!r}'
        cls.__context_instance.set(value)


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


