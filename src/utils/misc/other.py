import re

@property
def check_to_cyrillic(text: str):
    return re.search(r'[^\W\d]', text)

@property
def check_for_space(text: str) -> bool:
    if ' ' in text:
        return True
    return False

@property
def check_for_email_correct(email_text: str) -> bool:
    if '@' in email_text:
        return True
    return False
