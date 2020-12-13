import os
from glob import glob
from typing import List

from aiogram import types
from loguru import logger

from data.config import LOGS_BASE_PATH, ADMIN_IDS


def last_log():
    """
    Get last log from /logs/ folder
    :return:
    """
    logs_list: List = os.listdir(LOGS_BASE_PATH)
    full_list = [os.path.join(LOGS_BASE_PATH, i) for i in logs_list]
    time_sorted_list: List = sorted(full_list, key=os.path.getmtime)

    if not time_sorted_list:
        return
    return time_sorted_list[-1]


def delete_all_logs():
    to_remove = glob(f"{LOGS_BASE_PATH}/*.log")

    for files in to_remove:
        try:
            os.remove(files)
        except PermissionError:
            logger.info("PErmissio error, cant delete file")
            pass


async def get_logs(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        return

    file_ = last_log()

    if not file_:
        return await message.answer("Логов Нету ¯\_(ツ)_/¯")

    name_file = ''.join(file_)

    with open(name_file, "r") as file:
        lines = file.read()
        await message.answer(lines)


async def remove_logs(msg: types.Message):
    if msg.from_user.id in ADMIN_IDS:
        return
    try:
        delete_all_logs()
    except Exception as e:
        logger.exception(e)
        return await msg.answer(str(e))
    logger.info("All logs removed from logs base path!")
    await msg.answer(f"Удлаены все логи в Директории, {LOGS_BASE_PATH}/")


