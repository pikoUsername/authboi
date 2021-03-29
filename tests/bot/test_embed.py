import os

from unittest.mock import Mock

from iternal.bot.utils.embed import EmbedFieldPaginator, Embed, Field


def test_embed():
    title = "test"

    e = Embed(title)

    assert str(e) == f"<strong>{title}</strong>\n"


def test_embed_title():
    title = "test"

    e = Embed(title)
    assert e.title == f"<strong>{title}</strong>"


def test_embed_add_field():
    title = "test"

    ftitle = "test"
    e = Embed(title)
    e.add_field(ftitle, ftitle)
    assert e.fields[0].title == ftitle


def test_field_creation():
    title = "text"
    text = "title"

    f = Field(Mock(), title, text, 0x1)  # using bytes, bc looks cool

    assert f.title == title
    assert f.text == text
    assert f.index == 0x1


def test_embed_paginator():
    e = EmbedFieldPaginator(title="hahahaha")

    pr = os.urandom(20).hex()
    e.add_field(pr, pr)

    # bad code, i understood
    for f in e:
        assert f.get_embed() == f"\n\t<strong >{pr}</strong>\t{pr}\n"
