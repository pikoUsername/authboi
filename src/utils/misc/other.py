import re

def check_to_cyrillic(text: str):
    return re.search(r'[^\W\d]', msg.text)
