from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from src.states.user.exit import Exit
from src.loader import db
from src.models.models import db_


async def remove_user(msg: types.Message):
    user = await db.get_user(msg.from_user.id)
    if not user:
        return await msg.answer("Вы не авторизованы как польветель")

    await msg.answer("Вы уверены в этом?\n Если да то введите ваш Пароль от учетной, \n для доказтельства что это вы")
    logger.info(f"user: {user.username} started to removing account")
    await Exit.wait_to_password.set()

async def user_pass_verify(msg: types.Message, state: FSMContext):
    user = await db.get_user(msg.from_user.id)

    current_password = user.password

    if current_password == msg.text:
        logger.info("user verified password")
        async with state.proxy() as data:
            data["user"] = user
        await Exit.wait_to_accept.set()
        await msg.delete()
        return await msg.answer("Вы потвердили что это вы теперь Подвердите ВЫ точно хоите этого?")
    await msg.answer("Не правльный пароль\n отмена /cancel")


async def user_rm_accept(msg: types.Message, state: FSMContext):
    if msg.text in ['Y', 'y']:
        async with state.proxy() as data:
            user = data["user"]
        try:
            logger.info(f"user: {msg.from_user.username} account was removed")
            await user.delete()
            await state.finish()
            return await msg.answer("Вы успешно удалили Свою учетную запись!")
        except Exception as e:
            logger.exception(f"ERROR: {e}")
            await state.finish()
            return await msg.answer("Пройзошла непредвиденная ошибка! 500")
    elif msg.text in ["N", "n"]:
        await state.finish()
        await msg.answer("Вы отменили действие!")
    else:
        await msg.answer("Повтрите еще раз!")