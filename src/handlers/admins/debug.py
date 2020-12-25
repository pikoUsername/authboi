import os
from glob import glob
from typing import List
from math import ceil
import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Command
from loguru import logger

from src.data.config import LOGS_BASE_PATH
from src.loader import dp, db


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
            pass


def parting(xs, parts):
    part_len = ceil(len(xs)/parts)
    return [xs[part_len*k:part_len*(k+1)] for k in range(parts)]


@dp.message_handler(Command(["logs", "get_logs"]), chat_type='private', state="*")
async def get_logs(msg: types.Message):
    user = await db.get_user(msg.from_user.id)

    if not user:
        return await msg.answer("Авторизуйтесь для этого!")

    if not user.is_admin:
        return await msg.answer("Вы не Админ")

    logger.info("Logs getted")
    loop = asyncio.get_event_loop()
    file_ = last_log()

    if not file_:
        return await msg.answer("Логов Нету ¯\_(ツ)_/¯")

    name_file = ''.join(file_)

    with open(name_file, "r") as file:
        lines = file.read()

        if len(lines) <= 4027:
            return await msg.answer(f"{lines}")

        whole_log = await loop.run_in_executor(None, parting, lines, 5)
        for peace in whole_log:
            await msg.answer(f"{peace}")
            await asyncio.sleep(0.1)

@dp.message_handler(Command("remove_all_logs"), state="*")
async def remove_logs(msg: types.Message):
    logger.info("removing logs...")
    user = await db.get_user(msg.from_user.id)

    if not user:
        return await msg.answer("Авторизуйтесь для этого!")

    if not user.is_admin:
        return

    try:
        delete_all_logs()
    except Exception as e:
        logger.exception(e)
        return await msg.answer(str(e))

    logger.info("All logs removed from logs base path!")
    await msg.answer(f"Удлаены все логи в Директории, {LOGS_BASE_PATH}/")


