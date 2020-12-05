from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes
from loguru import logger

from authboi.src.states.user.auth import StartState

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

    await StartState.next()
    await msg.answer("Теперь ввидите ваш пароль, если хотите конечно.\n Вас никто не заставляет.\n всегда есть комманда /cancel")

async def bot_auth_password(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["password"] = msg.text

    await StartState.next()
    await msg.answer("Теперь вы уверены, вы этом Y/N, если нет,\n то можете посто написать комманду /cancel,\n или если хотите что то изменить то /back")

async def bot_auth_back(msg: types.Message):
    await StartState.previous()

    await msg.answer("Вы сделали шаг назад, это непримелимо.\n Но терпимо если вы ошиблись!")

@dp.message_handler(state=StartState.wait_to_accept, content_types=ContentTypes.TEXT)
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


