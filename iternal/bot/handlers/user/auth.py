from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.webhook import SendMessage, EditMessageText
from aiogram.types import ContentTypes
from loguru import logger

from iternal.bot.states.user.auth import StartState
from iternal.bot.loader import db, dp
from iternal.bot.utils.misc import fill_auth_final


@dp.message_handler(Command("cancel"), state="*")
async def bot_cancel_handler(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if not current_state:
        return
    await state.finish()
    return SendMessage(msg.chat.id, "Действие было Отмменено!")


@dp.callback_query_handler(text="start_login")
async def bot_start_auth(call_back: types.CallbackQuery):
    await StartState.wait_to_login.set()

    logger.info("Some one started authorization")
    return EditMessageText("Вы начали Авторизацию! так что ввидите Имя или Логин",
                           call_back.message.chat.id,
                           message_id=call_back.message.message_id)


@dp.message_handler(state=StartState.wait_to_login, content_types=ContentTypes.TEXT)
async def bot_auth_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if ' ' in message.text:
            return SendMessage(message.chat.id,
                               "Не правльное Имя, пробелы должны быть заменены на - или что то подобное.")

        data["login"] = message.text

        logger.info("seme one getted login", message.text)

    await StartState.wait_to_email.set()
    return SendMessage(message.chat.id, "Теперь ввидите ваш эмейл, если можно\n"
                       "Всегда будет и всегда с нами комманда /cancel,\n и его брат /back")


@dp.message_handler(state=StartState.wait_to_email, content_types=ContentTypes.TEXT)
async def bot_auth_email(msg: types.Message, state: FSMContext):
    if ' ' in msg.text:
        return SendMessage(msg.chat.id, "Вы не правильно ввели эмейл, Там не должно быть пробелов")
    elif '@' not in msg.text:
        return SendMessage(msg.chat.id, "Вы не правльно ввели эмейл,\n так как Эмейл не имеет знака - '@'")

    logger.info(f"getted email, email {msg.text}")
    async with state.proxy() as data:
        data["email"] = msg.text

    await StartState.wait_to_password.set()
    return SendMessage(msg.chat.id, "Теперь ввидите ваш пароль, если хотите конечно.\n "
                       "Вас никто не заставляет.\n всегда есть комманда /cancel.")


@dp.message_handler(state=StartState.wait_to_password, content_types=ContentTypes.TEXT)
async def bot_auth_password(msg: types.Message, state: FSMContext):
    if ' ' in msg.text:
        return SendMessage(msg.chat.id, "В пароле содержатся символ пробел. Это недопустимо!")
    elif len(msg.text) <= 8:
        return SendMessage(msg.chat.id, "Пароль Ненадежный, Это недопустимо!\n Он должен прывышать 8 символов")

    logger.info('password handler activated')
    async with state.proxy() as data:
        data["password"] = msg.text

    await msg.delete()

    await StartState.wait_to_verify_pass.set()
    return SendMessage(msg.chat.id, "Теперь ввидите ваш пароль снова!\n"
                       "Если вы забыли его то ввидите /cancel и авторизуйтесь снова!")


@dp.message_handler(state=StartState.wait_to_verify_pass, content_types=ContentTypes.TEXT)
async def bot_auth_password_verify(msg: types.Message, state: FSMContext):
    logger.info(f"Accept State, user: {msg.from_user.username}")
    async with state.proxy() as data:
        password_verify = data["password"]
        if password_verify != msg.text:
            return SendMessage(msg.chat.id, "Не правильный Пароль, Повторите еще раз!")
    await StartState.wait_to_accept.set()
    await msg.delete()
    return SendMessage(msg.chat.id, "Теперь вы уверены, вы этом Y/N, если нет,\n "
                       "то можете посто написать комманду /cancel,\n или если хотите что то изменить то /back")


@dp.message_handler(Command("back"), state="*")
async def bot_auth_back(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        return

    logger.info(f"Someone was backed to {current_state}")
    await StartState.previous()
    return SendMessage(msg.chat.id,
                       f"Вы сделали шаг назад, это непримелимо.\n "
                       f"Но терпимо если вы ошиблись!\n Вы на шаге {current_state[11:]}")


@dp.message_handler(text=("Y", "y", "yes"), state=StartState.wait_to_accept)
async def yes_auth_password(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        login = data["login"]
        password = data["password"]
        email = data["email"]
        logger.info(f"User authed, name:{msg.from_user.username}")
    try:
        await db.add_new_user(
            user=msg.from_user,
            login=login,
            email=email,
            password=password,
        )
    except Exception as e:
        logger.exception(e)
        return SendMessage(msg.chat.id,
                           "Ошибка попробуйте снова.\n"
                           "Может быть вашы данные совпали с другими аккаунтами!\n или ошибка в созданий аккаунта")

    text = fill_auth_final(password, login, email)
    await state.finish()
    logger.info('------USER AUTHORIZATION!------')
    logger.info(f"| login: {login} | email: {email}")
    return SendMessage(msg.chat.id, text)


@dp.message_handler(text=("n", "N"), state=StartState.wait_to_accept)
async def cancel_auth(msg: types.Message, state: FSMContext):
    await state.finish()
    logger.info("cancelled authorization")
    return SendMessage(msg.chat.id, "Вы отменили авторизацию!")


@dp.message_handler(state=StartState.wait_to_accept, content_types=ContentTypes.TEXT)
async def bot_auth_accept(msg: types.Message):
    return SendMessage(msg.chat.id, "Попробуйте снова!")
