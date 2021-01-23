from typing import Optional


def fill_auth_final(password: str, login: str, email: str) -> Optional[str]:
    password_len = len(password)
    pass_to_show = []
    for i in range(0, password_len):
        pass_to_show.append("*")

    text = [
        "Вы авторизованы как: ",
        f"Имя: {login}",
        f"email: {email}",
        "Пароль: ",
        "".join(pass_to_show),
    ]
    return "\n".join(text)
