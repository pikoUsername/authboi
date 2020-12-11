from aiogram import types
from aiogram.utils.callback_data import CallbackData

from src.keyboards.inline.start import choice_kb
from src.keyboards.inline.admin import admin_kb

async def get_statistic(call_back: types.CallbackQuery): # registered in 6 line __init__.py
    # here statistic

    await call_back.message.edit_text("Смотреть нечего")


async def get_users(call_back: types.CallbackQuery): # registered in 7 line __init__.py
    users_data = CallbackData('name', 'id')
    # here get all users in inline keyboard
    all_users_keyboard = types.InlineKeyboardMarkup()
    all_users_keyboard.add(types.InlineKeyboardButton("<< Назад", call_back="back_from_all_users"))

    await call_back.message.edit_reply_markup(all_users_keyboard)

async def from_all_users_back(call_back: types.CallbackQuery): # refister in __init__.py 8 line
    await call_back.message.edit_text("Админка: ", reply_markup=admin_kb)

async def some_notFeature(): # register in
    pass

async def back_admin_kb(call_back: types.CallbackQuery):
    admin_choice = choice_kb.add(types.InlineKeyboardButton("<< В админку", call_back="again_admin"))
    await call_back.message.edit_text("Выбирите: ", reply_markup=admin_choice)

async def again_to_admin_menu(call_back: types.CallbackQuery):
    await call_back.message.edit_text("Админка: ", reply_markup=admin_kb)
