from aiogram import types
from aiogram.utils.callback_data import CallbackData

from src.loader import db
from src.keyboards.inline.admin import admin_kb

async def get_statistic(call_back: types.CallbackQuery):
    # here statistic

    await call_back.message.edit_text("Смотреть нечего")


async def get_users(call_back: types.CallbackQuery):
    users_data = CallbackData('name', 'id')
    # here get all users in inline keyboard
    all_users = await db.get_all_users()
    all_users_keyboard = types.InlineKeyboardMarkup()
    for users in all_users:
        all_users_keyboard.row(types.InlineKeyboardButton(f"{users.name}", call_back="None"))
    all_users_keyboard.add(types.InlineKeyboardButton("<< Назад", call_back="back_from_all_users"))

    await call_back.message.edit_reply_markup(all_users_keyboard)

async def from_all_users_back(call_back: types.CallbackQuery):
    await call_back.message.edit_text("Админка: ")
    await call_back.message.edit_reply_markup(admin_kb)

async def