from typing import List, Optional

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.handler import Handler
from aiogram import types
from loguru import logger

from iternal.bot.utils.embed import Embed


class HelpCommandEmbed:
    """
    If you need Paginated Help command,
    so write yourself, not me,

    Parses All bot commands, from dispatcher handler
    and craetes with template command signature
    And Shows to client.

    lower very bad code...
    """
    __slots__ = "_dp", "embed"

    def __init__(self, dp: Dispatcher = None, embed: Embed = None):
        self.embed = embed or Embed("Справка")
        self._dp = dp

    @property
    def dp(self):
        if self._dp is None:
            self._dp = Dispatcher.get_current()
        return self._dp

    def get_command_signature(self, handler_obj: Handler.HandlerObj) -> str:
        # filters is tuple
        template = "{aliases} - {doc}"
        if handler_obj.filters:
            cmds = self.get_commands(handler_obj)
        else:
            return ""

        # i hope it will work
        # {aliases} - {doc}
        template.format(
            aliases=" | ".join(cmd.commands for cmd in cmds),
            doc=handler_obj.handler.__doc__,
        )

        return template

    def add_handler_to_help(
        self,
        handler_obj: Handler.HandlerObj,
    ) -> None:
        self.embed.add_field(
            self.get_command_signature(handler_obj),
            handler_obj.handler.__doc__ or "No Help Provided..."
        )

    def get_bot_help(self):
        all_commands = self.dp.message_handlers.handlers
        # when get_bot_help calls second time,
        # add_handler_to_help duplicate this.
        # it s unaccaptable
        if not self.embed.fields:
            for cmd in all_commands:
                self.add_handler_to_help(cmd)

        return self.embed.clean_embed

    def get_commands(self, handler_obj: Handler.HandlerObj) -> List[Command]:
        cmds = [f for f in handler_obj.filters if isinstance(f, Command)]
        return cmds

    def to_bot_command(
        self,
        alias: str = None,
        desc: str = None
    ) -> Optional[types.BotCommand]:
        if alias is None:
            return
        if desc is None:
            desc = "No Help provided..."

        cmd = types.BotCommand(alias, desc)
        return cmd

    async def handler(self, m: types.Message, *_):
        return await m.answer(self.get_bot_help())

    def setup(self, dp: Dispatcher = None) -> None:
        logger.debug("Setup help command.")
        dp = dp or self.dp

        dp.register_message_handler(self.handler, commands="help", state="*")

    def setup_handlers_to_telegram(self):
        all_commands = self.dp.message_handlers.handlers
        for cmd in all_commands:
            self.dp.bot.set_my_commands([
                self.to_bot_command(cmd.filters or h.__name__, h.__doc__)
                for h in cmd.handler
            ])
