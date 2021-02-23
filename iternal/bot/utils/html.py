import re

__all__ = "wrap_text_html", "strong_text", "a"

# represents Available HTML tags for telegram bot API
_AVAILABLE_TAGS = (
    "b",
    "strong",
    "i",
    "em",
    "strike",
    "s",
    "pre",
    "a",
    "code"
)  # set

# just adds " for attrubiute
# idk how to fix that
# but it uses ONLY in "a" tag and with "href" attr
ohoh = lambda text: '"' + text + '"'  # yes, i know is bad, but i cant make more netter


# note, tests in tests/bot/test_wrappers.py
def wrap_text_html(text: str, tag: str, **tags_attrubiutes) -> str:
    # i wont write available tags attribute
    assert tag in _AVAILABLE_TAGS, "Telegram not supported tag."

    attrs_tag = [f"{k}={ohoh(v)}" for k, v in tags_attrubiutes.items()] or ""

    result = f"<{tag} {''.join(attrs_tag)}>{text}</{tag}>"

    return result


def strong_text(text: str) -> str:
    # just wrap text with <strong> </strong>
    return wrap_text_html(text, "strong")


def a(text: str, url: str) -> str:
    assert re.search(r"^(http|https)://", url), "not correct url."
    return wrap_text_html(text, "a", href=url)