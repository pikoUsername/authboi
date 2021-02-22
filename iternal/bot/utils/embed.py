from __future__ import annotations

from typing import List, TypeVar, Type, Union

from gino.dialects.asyncpg import AsyncpgCursor

__all__ = "Embed", "Field", "wrap_text_html", "strong_text"

# represents Available HTML tags for telegram bot API
_AVAILABLE_TAGS = (
    "b",
    "strong",
    "i",
    "em",
    "strike",
    "s",
    "pre",
    "a"
)  # set

T = TypeVar("T")  # slut type

# just adds " for attrubiute
# idk how to fix that
# but it uses ONLY in "a" tag and with "href" attr
ohoh = lambda text: '"' + text + '"'  # yes, i know is bad, but i cant make more netter


# note, tests in tests/bot/test_wrappers.py
def wrap_text_html(text: str, tag: str, **tags_attrubiutes) -> str:
    # i wont write available tags attribute
    assert tag in _AVAILABLE_TAGS, "Telegram not supported tag."

    attrs_tag = [f"{k}={ohoh(v)}" if not isinstance(v, bool) else
                 k for k, v in tags_attrubiutes.items()] or ""

    pre_result = "<{tag} {attrs}>{text}</{tag}>"

    result = pre_result.format(
        tag=tag,
        attrs=''.join(attrs_tag),
        text=text,
    )

    return result


def strong_text(text: str) -> str:
    # just wrap text with <strong> </strong>
    return wrap_text_html(text, "strong")


class Embed:
    __slots__ = "_title", "value", "fields", "_fields_len"
    """
    Embed like discord, but more worse,
    maybe added pagination, for embed
    """
    def __init__(self, title: str, value=tuple()):
        if not isinstance(value, list):
            value = "".join(value)

        self.value = value

        self._title = title
        self.fields: List[Field] = []
        self._fields_len = 0

    # properties

    @property
    def title(self) -> str:
        return strong_text(self._title)

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
    Embed Paginator, fundament for TelegramEmbedPaginator.

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
        _title = strong_text(self.title)
        text = (
            f"\n\t{_title}"
            f"\t{self.text}\n",
        )
        return "".join(text)

    def __repr__(self):
        return self.get_embed()

    def copy(self):
        return self
