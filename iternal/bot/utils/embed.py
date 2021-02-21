from __future__ import annotations

from typing import List, TypeVar, Type

from aiogram.types import ParseMode

__all__ = "Embed", "Field", "wrap_text_html", "strong_text"

# represents Available HTML tags for telegram bot API
_AVAILABLE_TAGS = {
    "b",
    "strong",
    "i",
    "em",
    "strike",
    "s",
    "pre",
    "a"
}  # set, idk why do use it, but i think its efficent

T = TypeVar("T")  # slut type
# just adds " for attrubiute
# idk how to fix that
# but it uses ONLY in "a" tag
ohoh = lambda text: '"' + text + '"'  # yes, i know is bad, but i cant make more netter


# note, tests in tests/bot/test_wrappers.py
def wrap_text_html(text: str, tag: str, **tags_attrubiutes) -> str:
    # i wont write available tags attribute,
    assert tag != _AVAILABLE_TAGS, "Telegram not supported tag."

    attrs_tag = [f"{k}={ohoh(v)}" for k, v in tags_attrubiutes.items()] or ""

    pre_result = "<{tag} {attrs}>{text}</{tag}>"

    if not tags_attrubiutes:
        pre_result.replace(" ", "")

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
    __slots__ = "_title", "value", "fields", "__fields_len"
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
        self.__fields_len = 0

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

    def add_field(self, title: str, text: str, *, parse_mode: str = "HTML") -> None:
        assert parse_mode in dir(ParseMode), "Not correct parse_mode"

        field_to_add = self._create_field(embed=self, title=title, text=text)
        self.fields.append(field_to_add)
        self.__fields_len += 1

    def _create_field(self, *args, **kwargs) -> Field:
        if "index" in kwargs:
            del kwargs['index']

        field = Field(*args, index=self.__fields_len, **kwargs)
        return field

    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        self = cls.__new__(cls)

        self.title = data.get("title", None)
        self.value = data.get("value", None)

        return self


class EmbedPaginator(Embed):
    def __init__(self, per_page: int = 5, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.per_page = per_page

    def get_page(self, page: int):
        return self.fields[page]

    def has_perviuos_page(self):
        pass  # todo embed paginator


class Field:
    __slots__ = "text", "index", "embed", "title"

    def __init__(self, embed: Embed, title: str, text: str, index: int = 0):
        self.title = title
        self.text = text
        self.index = index
        self.embed = embed

    def get_embed(self) -> str:
        _title = strong_text(self.title)
        text = (
            f"\n\t{_title}"
            f"\t{self.text}\n",
        )
        return "".join(text)
