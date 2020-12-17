import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from src.states.user.auth import StartState
from src.loader import db
from data.config import ADMIN_IDS


async def bot_cancel_handler(msg: types.Message, state: FSMContext):
    """
    registered in 45 65 line __init__.py
    """
    # checking for corrent state!
    current_state = await state.get_state()
    if not current_state:
        return

    logger.info(f"Cancelling {await state.get_state()}")
    await state.finish()
    await msg.answer("Действие было Отмменено!")


async def bot_start_auth(call_back: types.CallbackQuery):
    await StartState.wait_to_login.set()

    logger.info("Some one started authorization")
    await call_back.message.edit_text("Вы начали Авторизацию! так что ввидите Имя или Логин")


async def bot_auth_login(message: types.Message, state: FSMContext):
    """
    checks for space and commits this changes
    registered in 67 line __init__.py

    """
    async with state.proxy() as data:
        if ' ' in message.text:
            return await message.answer("Не правльный Имя, пробелы должны быть заменены на - или что то подобное!")

        data["login"] = message.text

        logger.info("seme one getted login", message.text)

    await StartState.wait_to_email.set()
    await message.answer("Теперь ввидите ваш эмейл, если можно\n Всегда будет и всегда с нами комманда /cancel,\n и его брат /back")


async def bot_auth_email(msg: types.Message, state: FSMContext):
    """
    Checks for space and '@' if exists in text
    registered in 82 line __init__.py

    """
    if ' ' in msg.text:
        return await msg.answer("Вы не правильно ввели эмейл, Там не должно быть пробелов")
    elif not '@' in msg.text:
        return await msg.answer("Вы не правльно ввели эмейл,\n так как Эмейл не имеет знака - '@'")

    logger.info(f"getted email, email {msg.text}")
    async with state.proxy() as data:
        data["email"] = msg.text

    await msg.answer("Теперь ввидите ваш пароль, если хотите конечно.\n Вас никто не заставляет.\n всегда есть комманда /cancel.")
    await StartState.wait_to_password.set()


async def bot_auth_password(msg: types.Message, state: FSMContext):
    """
    delete message password,
    """
    check = re.search(r'[^\W\d]', msg.text)

    if not check:
        logger.info(f"Some one really stupid wants to type with russian words password FUCK!")
        return await msg.answer("В строке имеются символы керилицы!")
    elif ' ' in msg.text:
        return await msg.answer("В пароле содержатся символ пробел. Это недопустимо!")
    elif len(msg.text) <= 8:
        return await msg.answer("Пароль Ненадежный, Это недопустимо!\n Он должен прывышать 8 символов")

    logger.info('password handler activated')
    async with state.proxy() as data:
        data["password"] = msg.text

    await msg.delete()
    await msg.answer("Теперь ввидите ваш пароль снова! Если вы забыли его то ввидите /cancel и авторизуйтесь снова!")
    await StartState.wait_to_verify_pass.set()


async def bot_auth_password_verify(msg: types.Message, state: FSMContext):
    logger.info(f"Accept State, user: {msg.from_user.username}")
    async with state.proxy() as data:
        password_verify = data["password"]
        if password_verify != msg.text:
            return await msg.answer("Не правильный Пароль, Повторите еще раз!")
        await StartState.wait_to_accept.set()
        await msg.delete()
        await msg.answer("Теперь вы уверены, вы этом Y/N, если нет,\n то можете посто написать комманду /cancel,\n или если хотите что то изменить то /back")


async def bot_auth_back(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if not current_state:
        return

    logger.info(f"Someone was backed to {current_state}")
    await StartState.previous()
    await msg.answer(f"Вы сделали шаг назад, это непримелимо.\n Но терпимо если вы ошиблись!\n Вы на шаге {current_state[11:]}")


async def bot_auth_accept(msg: types.Message, state: FSMContext):
    if msg.text in ["Y", "y", "yes"]:
        await msg.answer("Вы теперь авторизованы как полноправный пользветель!")
        async with state.proxy() as data:
            login = data["login"]
            password = data["password"]
            email = data["email"]
            password_len = len(data["password"])
            pass_to_show = []
            logger.info(f"User authed, name:{msg.from_user.username}")

        for i in range(0, password_len):
            pass_to_show.append("*")

        text = [
            "Вы авторизованы как: ",
            f"Имя: {login}",
            f"email: {email}",
            f"Пароль: ",
            "".join(pass_to_show),
        ]

        await msg.answer("\n".join(text))
        logger.info('------USER AUTHORIZATION!------')
        logger.info(f"| login: {login} | email: {email} |")
        if msg.from_user.id in ADMIN_IDS:
            await db.add_new_user(
                login=login,
                email=email,
                password=password,
                is_admin=True,
            )
            await state.finish()
            return await msg.answer("Вы зарегестрированы как Админ")
        await db.add_new_user(
            login=login,
            email=email,
            password=password,
            is_admin=False,
        )

        await state.finish()

    elif msg.text in ["N", "n", "no"]:
        await msg.answer("Вы отменили авторизацию!")
        logger.info("cancelled authorization")
        return await state.finish()
    else:
        await msg.answer("Попробуйте снова!")
