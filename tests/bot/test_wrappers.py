from iternal.bot.utils.embed import wrap_text_html


def test_wrap_text_html():
    text = "LOL_KEK_CHEBUREK"
    result = wrap_text_html(text, "strong")  # strong style

    assert result == f"<strong >{text}</strong>"


def test_wrap_text_html_href():
    url = 'https://google.com'
    text = "lol"

    result = wrap_text_html(text, "a", href=url)

    assert result == f'<a href="{url}">{text}</a>'
