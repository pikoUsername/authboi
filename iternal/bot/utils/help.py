from typing import List, Union

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.handler import Handler
from loguru import logger

from iternal.bot.utils.embed import Embed


class HelpCommand:
    __slots__ = "dp", "embed", "prefix", "suffix"

    def __init__(self, prefix: str = "```", suffix: str = "```"):
        self.embed = Embed("Справка")
        self.dp = Dispatcher.get_current()
        self.prefix = prefix
        self.suffix = suffix

    def get_command_signature(self, handler_obj: Handler.HandlerObj):
        data: List[Command] = [
            f for f in handler_obj.filters if isinstance(f, Command)]

        # {aliases} - {doc}
        result = []
        for d in data:
            result.append(d)

        return data

    def add_handler(
        self,
        handler_obj: Handler.HandlerObj,
    ):
        self.embed.add_field(
            "".join(self.get_command_signature(handler_obj)),
            handler_obj.handler.__doc__ or "No Help Provided..."
        )

    def setup(self, dp: Dispatcher) -> None:
        logger.debug("Setup help command.")

        dp.register_message_handler(self.handler, commands="help", state="*")
