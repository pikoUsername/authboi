import re

__all__ = "wrap_text_html", "strong", "a", "code", "i"

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


# note, tests in tests/bot/test_wrappers.py
def wrap_text_html(text: str, tag: str, **tags_attrubiutes) -> str:
    assert tag in _AVAILABLE_TAGS, "Telegram not supported tag."
    attrs_tag = [f'{k}="{v}"' for k, v in tags_attrubiutes.items()] or ""
    result = f"<{tag} {''.join(attrs_tag)}>{text}</{tag}>"
    return result


def strong(text: str) -> str:
    # just wrap text with <strong> </strong>
    return wrap_text_html(text, "strong")


def a(text: str, url: str) -> str:
    assert re.search(r"^(http|https)://", url), "not correct url."
    return wrap_text_html(text, "a", href=url)


def code(s: str, lang: str) -> str:
    return wrap_text_html(s, "code", lang=lang)


def i(s: str):
    return wrap_text_html(s, "i")
