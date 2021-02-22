from typing import List

from aiogram.types import BotCommand, Message
from aiogram import Dispatcher
from loguru import logger

from iternal.bot.utils.embed import Embed


class HelpCommandParser:
    __slots__ = "commands", "embed"

    def __init__(self, commands: List[BotCommand]):
        self.commands = commands
        self.embed = Embed("Справка", "Справка для всех комманд, которые указаны. И доступны")

    def add_command(self, command: str, description: str):
        if not description.endswith("."):
            description += "."

        return self.embed.add_field(command + " - ", description)

    def setup_all_commands(self) -> None:
        for cmd in self.commands:
            self.add_command(cmd.command, cmd.description)

    async def handler(self, m: Message, *_):
        self.setup_all_commands()

        return await m.answer(self.embed.clean_embed)

    def setup(self, dp: Dispatcher) -> None:
        logger.debug("Setup help command.")

        dp.register_message_handler(self.handler, commands="help", state="*")
