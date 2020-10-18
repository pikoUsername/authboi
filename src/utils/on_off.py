from src.utils.misc.logging import logging

async def on_close(app):
    logging.warning("Goodbye So")
    await app["db"].close()

async def on_startup(app):
    from src.loader import bot
    from data.config import ADMIN_IDS

    logging.info("Bot started")

    await bot.send_message(chat_id=ADMIN_IDS, text="Бот запщен ХЫ" )
