from __future__ import annotations

from typing import List

from aiogram.types import ParseMode

__all__ = "Embed", "Field"


class Embed:
    __slots__ = "_title", "value", "fields", "__fields_len"
    """
    Embed like discord, but more worse,
    maybe added pagination, for embed
    """
    def __init__(self, title: str, value=None):
        if not isinstance(value, list):
            self.value = "".join(str(v) for v in value)
        else:
            self.value = value

        self._title = title
        self.fields: List[Field] = []
        self.__fields_len = 0

    # properties

    @property
    def title(self) -> str:
        return "<strong>" + self._title + "</strong>"

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

        field_to_add = self.create_field(embed=self, title=title, text=text)
        self.fields.append(field_to_add)
        self.__fields_len += 1

    def create_field(self, *args, **kwargs) -> Field:
        if "index" in kwargs:
            del kwargs['index']

        field = Field(*args, index=self.__fields_len, **kwargs)
        return field

    # magic methods, __init__ not included

    def __del__(self) -> None:
        for field in self.fields:
            field.clear()


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

    def clear(self) -> None:
        del self.embed.fields[self.index]
        self.embed = None

    def get_embed(self) -> str:
        text = (
            f"\t<strong>{self.title}</strong>\n",
            f"\t{self.text}\n",
        )
        return "".join(text)
