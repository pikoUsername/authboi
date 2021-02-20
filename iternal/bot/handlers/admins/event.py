from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, ChatTypeFilter
from aiogram.types import ContentType
from aiogram.utils.exceptions import BadRequest
from loguru import logger

from iternal.bot.loader import dp
from iternal.bot.keyboards.inline import inline_choice_event
from iternal.bot.states.user import InlineStates, EventState
from iternal.bot.utils import send_to_all_users


@dp.message_handler(
    ChatTypeFilter(chat_type="private"),
    commands="start_event",
    is_authed=True,
    is_admin=True, state="*"
)
async def start_event(msg: types.Message):
    await msg.answer("Укажите Будет ли там Инлайн Кнопка?", reply_markup=inline_choice_event)
    logger.info(f"Admin start create event, user_id {msg.from_user.id}")
    await EventState.wait_for_inline.set()


@dp.callback_query_handler(text="admin_event_inline_choice_yes", state=EventState.wait_for_inline)
async def admin_event_choice_yes(call_back: types.CallbackQuery):
    await call_back.message.edit_text("Хорошо Теперь Ввидите текст для инлайн кнопки")
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
async def admin_event_choice_no(call_back: types.CallbackQuery):
    await call_back.message.edit_text(
        "Теперь Пришлите Изображение,\n Вы можете просто Пропустить этап написав /skip.\n Отмена /cancel")
    await EventState.wait_for_image.set()


@dp.message_handler(state=EventState.wait_for_image, content_types=ContentType.PHOTO)
async def event_get_image(msg: types.Message, state: FSMContext):
    await msg.answer("Теперь Напишите текст который там будет")
    link = msg.photo[0:len(msg.photo)]

    async with state.proxy() as data:
        data["link"] = link

    await EventState.wait_for_text.set()


@dp.message_handler(Text(["skip", "s", "/skip"]), state=EventState.wait_for_image, content_types=ContentType.TEXT)
async def skip_photo_upload(msg: types.Message):
    await msg.answer("Теперь Напишите текст который там будет")
    await EventState.wait_for_text.set()


@dp.message_handler(state=EventState.wait_for_text)
async def write_text_file(msg: types.Message, state: FSMContext):
    """
    For text, and its bad code

    :param msg:
    :param state:
    :return:
    """
    if not msg.text:
        return await msg.answer("Отствует текст")

    await msg.answer("Теперь Вы Уверены в ЭТОМ? Y/N, PREVIEW:")
    safed_text = msg.text

    await EventState.wait_for_accept.set()

    async with state.proxy() as data:
        data["text"] = msg.text
        link = data.get("link", None)
        inline_text = data.get("inline_text", None)
        inline_url = data.get("inline_reference", None)

    # creating inline text and etc.
    if inline_text and inline_url:
        to_show_inline = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text=inline_text, url=inline_url),
            ]
        ], row_width=1)

        async with state.proxy() as data:
            data["inline_kb"] = to_show_inline

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
        inline_kb = data.get("inline_kb", None)
        link = data.get("link", None)
        text = data.get("text", None)

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
async def what_event(msg: types.Message):
    return await msg.answer("Повторите Снова!")
