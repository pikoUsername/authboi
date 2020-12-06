from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from src.states.user.auth import StartState
from src.utils.misc.other import check_to_cyrillic, check_for_space, check_for_email_correct

#TODO: Make request to database, and make db API

async def bot_cancel_handler(msg: types.Message, state: FSMContext):
    # checking for corrent state!
    current_state = await state.get_state()
    if not current_state:
        return

    logger.info("Cancelling authorazation")
    await state.finish()
    await msg.answer("Отмена авторизации!")


async def bot_auth_login(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not check_for_space:
            return await msg.answer("Не правльный Имя, пробелы должны быть заменены на - или что то подобное!")
        elif not check_to_cyrillic:
            return await msg.answer("Имя не должен содержать в себе кириллицу!")
        data["login"] = msg.text

        logger.info("seme one getted login", msg.text)

    await StartState.wait_to_email.set()
    await msg.answer("Теперь ввидите ваш эмейл, если можно\n Всегда будет и всегда с нами комманда /cancel,\n и его брат /back")

async def bot_auth_email(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not check_for_email_correct:
            return await msg.answer("Вы не правильно ввели Емейл,\n Бот поддерживает только 2 вида эмейлов,\n gmail, mail.ru нечего более")
        else:
            data["email"] = msg.text


    await msg.answer("Теперь ввидите ваш пароль, если хотите конечно.\n Вас никто не заставляет.\n всегда есть комманда /cancel.")
    await StartState.wait_to_password.set()


async def bot_auth_password(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # checking to cirilic in text
        check = check_to_cyrillic(msg.text)

        # cheking for spaces in password and etc.
        if not check:
            logger.info(f"Some one really stupid wants to type with russian words password FUCK!")
            return await msg.answer("В строке имеются символы керилицы!")
        elif ' ' in msg.text:
            return await msg.answer("В пароле содержатся символ пробел. Это недопустимо!")
        elif len(msg.text) <= 7:
            # check for len text and tip "better change it"
            await msg.answer("Пароль не надежный, лучше смените его!")

        data["password"] = msg.text

    await StartState.wait_to_accept.set()
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
            password_len = len(data["password"])
            pass_to_show = []

            for i in range(0, password_len):
                pass_to_show.append("*")

            text = [
                "Вы авторизованы как: ",
                f"Имя: {login}",
                f"Пароль: ",
                "".join(pass_to_show),
            ]

            await msg.answer("\n".join(text))

        await state.finish()

    elif msg.text in ["N", "n", "no"]:
        await msg.answer("Вы отменили авторизацию!")
        await state.finish()
    else:
        await msg.answer("Попробуйте снова!")

