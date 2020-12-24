from aiogram import types
from aiogram.dispatcher import FSMContext

from src.loader import db, dp
from src.keyboards.inline.event import inline_choice_event
from src.states.user.event import EventState

@dp.message_handler(types.ChatType.is_private, commands="start_event", state="*")
async def get_event_all(msg: types.Message):
    user = await db.get_user(msg.from_user.id)

    if not user:
        return

    if not user.is_admin:
        return await msg.answer("Вы не Админ")

    await msg.answer("Укажите Будет ли там Инлайн Кнопка?", reply_markup=inline_choice_event)
    await EventState.wait_for_inline.set()

@dp.callback_query_handler(text="admin_event_inline_choice_yes", state=EventState.wait_for_inline)
async def admin_event_choice_yes(msg: types.Message, state: FSMContext):
    pass

@dp.callback_query_handler(text="admin_event_inline_choice_no", state=EventState.wait_for_inline)
async def admin_event_choice_no(msg: types.Message, state: FSMContext):
    pass