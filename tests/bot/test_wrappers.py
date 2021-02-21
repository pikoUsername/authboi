from iternal.bot.utils.embed import wrap_text_html


def test_wrap_text_html():
    text = "LOL_KEK_CHEBUREK"
    result = wrap_text_html(text, "strong")  # italic style

    assert result == f"<strong>{text}</strong>"
