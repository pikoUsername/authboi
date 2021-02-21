from iternal.bot.utils.embed import EmbedPaginator, Embed


def test_embed():
    title = "test"

    e = Embed(title)

    assert e.clean_embed == f"<strong >{title}</strong>\n"


def embed_paginator():
    e = EmbedPaginator()

    pass  # todo Embed paginator
