@property
def check_for_email_correct(email_text: str) -> bool:
    if '@' in email_text:
        return True
    return False

