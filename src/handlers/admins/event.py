from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, ChatTypeFilter
from aiogram.types import ContentType
from loguru import logger

from src.loader import db, dp, bot
from src.keyboards.inline.event import inline_choice_event
from src.states.user.event import EventState
from src.states.user.inline import InlineStates
from src.utils.photo_link import photo_link_aiograph
from src.utils.spamer import send_to_all_users


@dp.message_handler(ChatTypeFilter(chat_type="private"), commands="start_event", state="*")
async def get_event_all(msg: types.Message):
    user = await db.get_user(msg.from_user.id)

    if not user:
        return False

    if not user.is_admin:
        return False

    await msg.answer("Укажите Будет ли там Инлайн Кнопка?", reply_markup=inline_choice_event)
    await EventState.wait_for_inline.set()


@dp.callback_query_handler(text="admin_event_inline_choice_yes", state=EventState.wait_for_inline)
async def admin_event_choice_yes(call_back: types.CallbackQuery, state: FSMContext):
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
async def admin_event_choice_no(call_back: types.CallbackQuery, state: FSMContext):
    await call_back.message.edit_text("Теперь Пришлите Изображение,\n Вы можете просто Пропустить этап написав /skip.\n Отмена /cancel")
    await EventState.wait_for_image.set()


@dp.message_handler(state=EventState.wait_for_image, content_types=ContentType.PHOTO)
async def event_get_image(msg: types.Message, state: FSMContext):
    photo = msg.photo[-1]

    await msg.bot.send_chat_action(msg.chat.id, 'upload_photo')
    await bot.send_chat_action(msg.chat.id)

    # link = await photo_link(photo)
    link = await photo_link_aiograph(photo)
    async with state.proxy() as data:
        data["link"] = link

    await msg.answer("Теперь Напишите текст который там будет")
    await EventState.wait_for_text.set()


@dp.message_handler(Text(["skip", "s", "/skip"]), state=EventState.wait_for_image, content_types=ContentType.TEXT)
async def skip_photo_upload(msg: types.Message, state: FSMContext):
    await msg.answer("Теперь Напишите текст который там будет")
    await EventState.wait_for_text.set()


@dp.message_handler(state=EventState.wait_for_text)
async def write_text_file(msg: types.Message, state: FSMContext):

    if not msg.text:
        return await msg.answer("Отствует текст")

    safed_text = msg.text

    async with state.proxy() as data:
        data["text"] = msg.text
        try:
            link = data["link"]
            inline_text = data["inline_text"]
            inline_url = data["inline_reference"]
        except KeyError:
            link = None
            inline_text = None
            inline_url = None

    await msg.answer("Теперь Вы Уверены в ЭТОМ? Y/N, PREVIEW:")
    await EventState.wait_for_accept.set()

    # creating inline text and etc.
    if inline_text or inline_url:
        to_show_inline = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text=inline_text, url=inline_url),
            ]
        ], row_width=1)

        async with state.proxy() as data:
            data["inline_kb"] = to_show_inline

        return await msg.answer_photo(photo=link, caption=safed_text, reply_markup=to_show_inline)
    if not link:
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
