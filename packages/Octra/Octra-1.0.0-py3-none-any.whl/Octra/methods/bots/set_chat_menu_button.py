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

from typing import Union

import Octra
from Octra import raw
from Octra import types


class SetChatMenuButton:
    async def set_chat_menu_button(
        self: "Octra.Client",
        chat_id: Union[int, str] = None,
        menu_button: "types.MenuButton" = None
    ) -> bool:
        """Change the bot's menu button in a private chat, or the default menu button.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the tarExtract chat.
                If not specified, default bot's menu button will be changed.

            menu_button (:obj:`~Octra.types.MenuButton`, *optional*):
                The new bot's menu button.
                Defaults to :obj:`~Octra.types.MenuButtonDefault`.
        """

        await self.invoke(
            raw.functions.bots.SetBotMenuButton(
                octra_user_id=await self.resolve_peer(chat_id or "me"),
                button=(
                    (await menu_button.write(self)) if menu_button
                    else (await types.MenuButtonDefault().write(self))
                )
            )
        )

        return True
