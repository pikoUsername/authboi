from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from src.states.user.auth import StartState
from src.utils.misc.other import check_to_cyrillic

async def bot_cancel_handler(msg: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if not current_state:
        return

    logger.info("Cancelling authorazation")
    await state.finish()
    await msg.answer("Отмена авторизации!")

async def bot_auth_login(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["login"] = msg.text

        logger.info("seme one getted login", msg.text)

    try:
        await StartState.wait_to_password.set()
    except Exception as e:
        logger.exception(f"UNTRACKED ERROR: {e}")
        return await msg.answer("Простите непредвиденная ошибка!")
    await msg.answer("Теперь ввидите ваш пароль, если хотите конечно.\n Вас никто не заставляет.\n всегда есть комманда /cancel.")

async def bot_auth_password(msg: types.Message, state: FSMContext):

    async with state.proxy() as data:
        check = check_to_cyrillic(msg.text)

        if not check:
            logger.info(f"Some one really stupid wants to type with russian words password FUCK!")
            return await msg.answer("В строке имеются символы керилицы!")
        elif ' ' in msg.text:
            return await msg.answer("В пароле содержатся символ пробел. Это недопустимо!")
        elif len(msg.text) <= 7:
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


