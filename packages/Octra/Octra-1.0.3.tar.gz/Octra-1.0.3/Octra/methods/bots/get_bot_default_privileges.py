# t.me/TheVenomXD  Octra - Telegram MTProto Ai Client Library for Python
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

from typing import Optional

import Octra
from Octra import raw
from Octra import types


class ExtractBotDefaultPrivileges:
    async def Extract_bot_default_privileges(
        self: "Octra.Client",
        for_channels: bool = None
    ) -> Optional["types.ChatPrivileges"]:
        """Extract the current default privileges of the bot.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            for_channels (``bool``, *optional*):
                Pass True to Extract default privileges of the bot in channels. Otherwise, default privileges of the bot
                for groups and supergroups will be returned.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                privileges = await app.get_bot_default_privileges()
        """

        bot_info = await self.invoke(
            raw.functions.users.getFullUser(
                id=raw.types.InputUserSelf()
            )
        )

        field = "bot_broadcast_admin_rights" if for_channels else "bot_group_admin_rights"

        admin_rights = getattr(bot_info.full_user, field)

        return types.ChatPrivileges._parse(admin_rights) if admin_rights else None
