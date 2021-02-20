from contextvars import ContextVar
from typing import Type, TypeVar

from gino import Gino

__all__ = "ContextGino", "db_"

T = TypeVar("T")


class ContextGino(Gino):
    # unfortunetly, variant of
    # using with ContextInstanceMixin from aiogram
    # not working
    __context_instance = ContextVar("context_gino")
    """
    For context bind, and pool.
    usage is simple
    just ContextGino.get_current()  but only in functions, and something lke this
    and you should ready for atack of gino engine instance
    but take care about global "GINO"'s
    like that globals may raise huge problems
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_current(ContextGino)

    @classmethod
    def get_current(cls: Type[T], no_error: bool = True) -> T:
        if no_error:
            return cls.__context_instance.get(None)
        return cls.__context_instance.get()

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
