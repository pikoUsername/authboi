import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, ChatTypeFilter
from aiogram.types import ContentType
from aiogram.utils.exceptions import BadRequest
from loguru import logger

from src.loader import db, dp
from src.keyboards.inline.event import inline_choice_event
from src.states.user.event import EventState
from src.states.user.inline import InlineStates
from src.utils.spamer import send_to_all_users


@dp.message_handler(ChatTypeFilter(chat_type="private"), commands="start_event", state="*")
async def start_event(msg: types.Message):
    user = await db.get_user(msg.from_user.id)

    if not user:
        return False

    if not user.is_admin:
        return False

    await msg.answer("Укажите Будет ли там Инлайн Кнопка?", reply_markup=inline_choice_event)
    logger.info(f"Admin start create event, user_id {user.user_id}")
    await EventState.wait_for_inline.set()


@dp.callback_query_handler(text="admin_event_inline_choice_yes", state=EventState.wait_for_inline)
async def admin_event_choice_yes(call_back: types.CallbackQuery, state: FSMContext):
    await call_back.message.edit_text("Хорошо Теперь Ввидите текст для инлайн кнопки")
    logger.info("Yes Event")
    await InlineStates.wait_for_inline_text.set()


@dp.message_handler(state=InlineStates.wait_for_inline_text)
async def write_text_to_inline(msg: types.Message, state: FSMContext):
    await msg.answer("Теперь Ввидите Ccылку для кнопки,\n Вы можете отменить действие с помощью /cancel")

    async with state.proxy() as data:
        data["inline_text"] = msg.text
    await InlineStates.wait_for_reference.set()


@dp.message_handler(state=InlineStates.wait_for_reference)
async def write_reference_inline(msg: types.Message, state: FSMContext):
    await msg.answer("Теперь Пришлите Изображение,\n Вы можете просто Пропустить этап написав /skip.\n Отмена /cancel")

    async with state.proxy() as data:
        data["inline_reference"] = msg.text
    await EventState.wait_for_image.set()


@dp.callback_query_handler(text="admin_event_inline_choice_no", state=EventState.wait_for_inline)
async def admin_event_choice_no(call_back: types.CallbackQuery, state: FSMContext):
    await call_back.message.edit_text("Теперь Пришлите Изображение,\n Вы можете просто Пропустить этап написав /skip.\n Отмена /cancel")
    await EventState.wait_for_image.set()


@dp.message_handler(state=EventState.wait_for_image, content_types=ContentType.PHOTO)
async def event_get_image(msg: types.Message, state: FSMContext):
    await msg.answer("Теперь Напишите текст который там будет")
    link = msg.photo[0:len(msg.photo)]

    async with state.proxy() as data:
        data["link"] = link

    await EventState.wait_for_text.set()


@dp.message_handler(Text(["skip", "s", "/skip"]), state=EventState.wait_for_image, content_types=ContentType.TEXT)
async def skip_photo_upload(msg: types.Message, state: FSMContext):
    await msg.answer("Теперь Напишите текст который там будет")
    await EventState.wait_for_text.set()


@dp.message_handler(state=EventState.wait_for_text)
async def write_text_file(msg: types.Message, state: FSMContext):
    first_time = time.monotonic()
    if not msg.text:
        return await msg.answer("Отствует текст")

    await msg.answer("Теперь Вы Уверены в ЭТОМ? Y/N, PREVIEW:")
    safed_text = msg.text

    await EventState.wait_for_accept.set()

    async with state.proxy() as data:
        data["text"] = msg.text
        try:
            link = data["link"]
        except KeyError:
            link = None
        try:
            inline_text = data["inline_text"]
            inline_url = data["inline_reference"]
        except KeyError:
            inline_text = None
            inline_url = None

    # creating inline text and etc.
    if inline_text and inline_url:
        to_show_inline = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text=inline_text, url=inline_url),
            ]
        ], row_width=1)

        async with state.proxy() as data:
            data["inline_kb"] = to_show_inline

        logger.info(f"Time handled of func write_text_file: {(first_time - time.monotonic()) * 1000} ")
        if not link:
            try:
                return await msg.answer(safed_text, reply_markup=to_show_inline)
            except BadRequest:
                return
        return await msg.answer_photo(photo=link, caption=safed_text, reply_markup=to_show_inline)
    return await msg.answer(safed_text)


@dp.message_handler(Text(['Y', 'y']), state=EventState.wait_for_accept)
async def send_all_event(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            inline_kb = data["inline_kb"]
            link = data["link"]
        except KeyError:
            link = None
            inline_kb = None
        text = data["text"]
    try:
        await send_to_all_users(text, link, inline_kb)
        await state.reset_data()
    except Exception as e:
        logger.error(e)
        await msg.answer("Ошибка невозможно прислать всем Пользветелям сообщение")


@dp.message_handler(Text(['N', 'n']), state=EventState.wait_for_accept)
async def cancel_event(msg: types.Message, state: FSMContext):
    await msg.answer("Отмена Формирования евента")
    logger.info("Canceled Event send.")

    await state.finish()


@dp.message_handler(state=EventState.wait_for_accept)
async def what_event(msg: types.Message, state: FSMContext):
    return await msg.answer("Повторите Снова!")
