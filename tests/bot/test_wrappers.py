import time

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


def test_wrap_deep():
    url = "https://google.com"
    text = "lol"
    result = wrap_text_html(wrap_text_html(text, "a", href=url), "code")
    assert result == f'<code ><a href="{url}">{text}</a></code>'


def test_html_wrap_perf():
    ftime = time.perf_counter() * 1000
    wrap_text_html("text", "a", href="#")
    t = time.perf_counter() * 1000 - ftime
    assert t < 0.099
