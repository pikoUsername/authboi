def test_embed():
    from iternal.bot.utils.embed import Embed

    title = "test"

    e = Embed(title)

    assert e.clean_embed == f"<h1>{title}</h1>"
