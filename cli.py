
async def on_startup(dp):
    from src import filters
    from src import middlewares
    from src.handlers import user, error

    error.setup(dp)
    user.setup(dp)
    filters.setup(dp)
    middlewares.setup(dp)

    from src.handlers.admins.notify_admins import notify_admins
    await notify_admins(dp)


if __name__ == '__main__':
    from aiogram import executor
    from src.loader import dp

    executor.start_polling(dp, on_startup=on_startup)