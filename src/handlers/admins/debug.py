import os
from glob import glob
from typing import List
from math import ceil
import asyncio

from aiogram import types
from loguru import logger

from src.config import LOGS_BASE_PATH
from src.loader import dp


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
    part_len = ceil(len(xs) / parts)
    return [xs[part_len * k:part_len * (k + 1)] for k in range(parts)]


@dp.message_handler(commands=("logs", "get_logs"), is_admin=True, chat_type='private', state="*")
async def get_logs(msg: types.Message):
    logger.info("Logs getted")
    file_ = last_log()

    if not file_:
        return await msg.answer("Логов Нету")

    name_file = ''.join(file_)

    with open(name_file, "r") as file:
        lines = file.read()

        if len(lines) <= 4027:
            return await msg.answer(f"{lines}")

        whole_log = parting(lines, 5)
        for peace in whole_log:
            await msg.answer(f"{peace}")
            await asyncio.sleep(0.1)


@dp.message_handler(commands="remove_all_logs", is_admin=True, state="*")
async def remove_logs(msg: types.Message):
    logger.info("removing logs...")
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, delete_all_logs)
    except Exception as e:
        logger.exception(e)
        return await msg.answer(str(e))

    logger.warning("All logs removed from logs base path!")
    await msg.answer(f"Удлаены все логи в Директории, {LOGS_BASE_PATH}/")
