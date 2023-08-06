# t.me/TheVenomXD  Octra - Telegram MTProto API Client Library for Python
# t.me/TheVenomXD  Copyright (C) 2017-present Akash <https://github.com/DesiNobita>
# t.me/TheVenomXD
# t.me/TheVenomXD  This file is part of Octra.
# t.me/TheVenomXD
# t.me/TheVenomXD  Octra is free software: you can redistribute it and/or modify
# t.me/TheVenomXD  it under the terms of the GNU Lesser General Public License as published
# t.me/TheVenomXD  by the Free Software Foundation, either version 3 of the License, or
# t.me/TheVenomXD  (at your option) any later version.
# t.me/TheVenomXD
# t.me/TheVenomXD  Octra is distributed in the hope that it will be useful,
# t.me/TheVenomXD  but WITHOUT ANY WARRANTY; without even the implied warranty of
# t.me/TheVenomXD  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# t.me/TheVenomXD  GNU Lesser General Public License for more details.
# t.me/TheVenomXD
# t.me/TheVenomXD  You should have received a copy of the GNU Lesser General Public License
# t.me/TheVenomXD  along with Octra.  If not, see <http://www.gnu.org/licenses/>.

from typing import List

import Octra
from Octra import raw
from Octra import types


class SetBotCommands:
    async def set_bot_commands(
        self: "Octra.Client",
        commands: List["types.BotCommand"],
        scope: "types.BotCommandScope" = types.BotCommandScopeDefault(),
        language_code: str = "",
    ) -> bool:
        """Set the list of the bot's commands.
        The commands passed will overwrite any command set previously.
        This method can be used by the own bot only.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            commands (List of :obj:`~Octra.types.BotCommand`):
                A list of bot commands.
                At most 100 commands can be specified.

            scope (:obj:`~Octra.types.BotCommandScope`, *optional*):
                An object describing the scope of users for which the commands are relevant.
                Defaults to :obj:`~Octra.types.BotCommandScopeDefault`.

            language_code (``str``, *optional*):
                A two-letter ISO 639-1 language code.
                If empty, commands will be applied to all users from the given scope, for whose language there are no
                dedicated commands.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                from Octra.types import BotCommand

                # t.me/TheVenomXD Set new commands
                await app.set_bot_commands([
                    BotCommand("start", "Start the bot"),
                    BotCommand("settings", "Bot settings")])
        """

        return await self.invoke(
            raw.functions.bots.SetBotCommands(
                commands=[c.write() for c in commands],
                scope=await scope.write(self),
                lang_code=language_code,
            )
        )
