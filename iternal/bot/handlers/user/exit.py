from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher.webhook import SendMessage, DeleteMessage
from aiogram.types import ContentType
from loguru import logger

from iternal.bot.states.user.exit import Exit
from iternal.bot.loader import dp
from iternal.store.user import User


@dp.message_handler(Command("remove"), is_authed=True)
async def remove_user(msg: types.Message):
    await Exit.wait_to_password.set()
    return SendMessage(msg.chat.id,
                       "Вы уверены в этом?\n Если да то введите ваш Пароль от учетной, \n для доказтельства что это вы")


@dp.message_handler(state=Exit.wait_to_password, content_types=ContentType.TEXT)
async def user_pass_verify(msg: types.Message, state: FSMContext, user: User):
    if user.password != msg.text:
        return SendMessage(msg.chat.id, "Не правльный пароль\n отмена /cancel")
    logger.info("user verified password")
    async with state.proxy() as data:
        data["user"] = user
    await Exit.wait_to_accept.set()
    DeleteMessage(msg.chat.id, msg.message_id)
    return SendMessage(msg.chat.id,
                       "Вы потвердили что это вы, теперь Подвердите Вы точно хоите этого? Y/N")


@dp.message_handler(text=("Y", "y", "yes"), state=Exit.wait_to_accept)
async def remove_user_fully(msg: types.Message, state: FSMContext, user: User):
    try:
        await user.delete()
        logger.info(f"user: {msg.from_user.username} account was removed")
        await msg.delete()
        await msg.answer("Вы успешно удалили Свою учетную запись.")
    except Exception as e:
        logger.exception(f"ERROR: {e}")
        await msg.answer("Пройзошла непредвиденная ошибка!")
    await state.finish()


@dp.message_handler(Text(["N", 'n', "no"]), state=Exit.wait_to_accept)
async def cancel_rm_user(msg: types.Message, state: FSMContext):
    await state.finish()
    return SendMessage(msg.chat.id, "Вы отменили действие!")


@dp.message_handler(state=Exit.wait_to_accept, content_types=ContentType.TEXT)
async def user_rm_accept(msg: types.Message):
    return SendMessage(msg.chat.id, "Повтрите еще раз!")
