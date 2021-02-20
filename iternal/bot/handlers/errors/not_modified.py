from aiogram.utils import exceptions

from iternal.bot.loader import dp


@dp.errors_handler(exceptions.MessageNotModified)
async def message_not_modified(*_):  # unused error handler, and arguments
    return True


@dp.errors_handler(exceptions.MessageToDeleteNotFound)
async def message_to_delete_not_found(*_):
    return True
