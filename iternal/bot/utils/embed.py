from __future__ import annotations

from typing import List, TypeVar, Type, Union, Any, Optional

__all__ = "Embed", "Field"

from aiogram import Dispatcher
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.utils.callback_data import CallbackData

from iternal.bot.utils.html import strong

T = TypeVar("T")  # slut type


class InvalidPage(Exception): pass


_DEFAULT_KB = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton("<<", callback_data="pervious_page"),
        InlineKeyboardButton(">>", callback_data="next_page"),
    ]
], row_width=4)

pagination_call = CallbackData("paginator", "key", "page")


class Embed:
    __slots__ = "_title", "value", "fields", "_fields_len"
    """
    Embed like discord, but more worse,
    maybe added pagination, for embed
    """
    def __init__(self, title: str, value=tuple()):
        if not isinstance(value, list):
            value = "".join(value)

        self.value = value if not value else f"{value}\n"

        self._title = title
        self.fields: List[Field] = []
        self._fields_len = 0

    # properties

    @property
    def title(self) -> str:
        return strong(self._title)

    @property
    def clean_embed(self) -> str:
        result = [self.title, self.value]

        for r in self.fields:
            res = r.get_embed()
            result.append(res)

        return "\n".join(result)

    # methods

    def add_field(self, title: str, text: str) -> None:
        field_to_add = self._create_field(
            index=self._fields_len,
            embed=self,
            title=title,
            text=text
        )
        self.fields.append(field_to_add)
        self._fields_len += 1

    def _create_field(self, *args, **kwargs) -> Field:
        field = Field(*args, **kwargs)
        return field

    def change_field(self, index: int, **kwargs):
        f = self.fields[index]
        f_dir = [a for a in f.__dir__() if not a.startswith("__")]
        for k, v in kwargs.items():
            if k in f_dir:
                setattr(f, k, v)
        self.fields[index] = f
        return self.fields[index]

    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        self = cls.__new__(cls)

        self.title = data.get("title", None)
        self.value = data.get("value", None)

        return self


class EmbedFieldPaginator(Embed):
    """
    Embed Paginator created like django paginator, but a it difference.
    """
    __slots__ = "_current_field", "per_field"

    def __init__(self, per_page: int = 5, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._current_field = 0
        self.per_field = per_page

    def get_field(self, page: int):
        try:
            return self.fields[page:self.per_field]
        except IndexError as exc:
            if self.fields:
                if self.has_pervious_page():
                    return self.get_field(page - 1)
            raise exc

    def has_pervious_page(self) -> bool:
        return self._current_field > 1

    def has_next_page(self) -> bool:
        return self._current_field <= self._fields_len

    def next(self) -> Field:
        field = self.get_field(self._current_field + 1)
        self._current_field += 1
        return field

    def pervious(self) -> Field:
        if self._current_field < 1:
            field = self.get_field(self._current_field - 1)
            self._current_field -= 1
        else:
            field = self.get_field(self._current_field)
        return field

    def __iter__(self):
        if self.has_next_page():
            return iter(self.next())


class Paginator:
    __slots__ = ("page_list", "per_page", "current_page",
                 "message", "dp")

    def __init__(self, object_list: List[Any], per_page: int = 1, dp=None):
        self.page_list = object_list
        self.per_page = int(per_page)
        self.current_page = 0
        self.dp = dp or Dispatcher.get_current()
        self.message = None

    @property
    def page_range(self) -> range:
        return range(0, len(self.page_list))

    def page(self, page: int) -> Optional[Union[Any, List[Any]]]:
        if page > self.num_pages:
            return ""
        if self.per_page == 1:
            return self.page_list[page]
        else:
            base = page * self.per_page
            try:
                return self.page_list[base:base + self.per_page]
            except IndexError:
                return None

    def page_number(self):
        return len(self.page_list)

    def next(self):
        self.current_page += 1
        return self.page(self.current_page)

    def pervious(self):
        self.current_page -= 1
        return self.page(self.current_page)

    @property
    def num_pages(self):
        return len(self.page_list)

    def has_next(self):
        return self.current_page <= self.num_pages

    def has_previous(self):
        return self.current_page > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.current_page + 1

    def previous_page_number(self):
        return self.current_page - 1

    async def start(self, m: Optional[Message] = None):
        if hasattr(self, 'message') and m is None:
            raise TypeError("Message and arguemnt 'm' is None")

        if m is not None:
            self.message = m

        self.dp.register_callback_query_handler(
            self.page_kb_handler, state="*")

    @staticmethod
    def get_page_keyboard(max_pages: int, key="example", page: int = 1):
        # Клавиатура будет выглядеть вот так:
        # |<< | <5> | >>|

        previous_page = page - 1
        previous_page_text = "<< "

        current_page_text = f"<{page}>"

        next_page = page + 1
        next_page_text = " >>"

        markup = InlineKeyboardMarkup()
        if previous_page > 0:
            markup.insert(
                InlineKeyboardButton(
                    text=previous_page_text,
                    callback_data=pagination_call.new(key=key, page=previous_page)
                )
            )

        markup.insert(
            InlineKeyboardButton(
                text=current_page_text,
                callback_data=pagination_call.new(key=key, page="current_page")
            )
        )

        if next_page < max_pages:
            markup.insert(
                InlineKeyboardButton(
                    text=next_page_text,
                    callback_data=pagination_call.new(key=key, page=next_page)
                )
            )

        return markup

    async def page_kb_handler(self, query: CallbackQuery, cd: dict):
        page = int(cd.get("page"))
        kb = self.get_page_keyboard(self.num_pages, cd.get("key"), page)
        await query.message.edit_text(self.page(page), reply_markup=kb)


class Field:
    __slots__ = "text", "index", "embed", "title"

    def __init__(
        self,
        embed: Union[Embed, EmbedFieldPaginator],
        title: str,
        text: str,
        index: int = 0
    ) -> None:
        self.title = title
        self.text = text
        # for embed paginator
        self.index = index
        self.embed = embed

    def get_embed(self) -> str:
        _title = strong(self.title)
        return f"{_title}\n{self.text}"

    @classmethod
    def from_dict(cls, **kwargs: Any) -> T:
        a = cls.__new__(cls)

        d = [elem for elem in dir(a)
             if not elem.startswith("__") and not callable(elem)]

        for k, v in kwargs.items():
            if k in d:
                setattr(a, k, v)

        return a

    __str__ = get_embed
    __repr__ = get_embed
