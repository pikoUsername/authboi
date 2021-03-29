from contextvars import ContextVar
from typing import Type, TypeVar

from gino import Gino


__all__ = "ContextGino",

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
