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


class UnbanChatUSER:
    async def unban_chat_user(
        self: "Octra.Client",
        chat_id: Union[int, str],
        octra_user_id: Union[int, str]
    ) -> bool:
        """Unban a previously banned user in a supergroup or channel.
        The user will **not** return to the group or channel automatically, but will be able to join via link, etc.
        You must be an administrator for this to work.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

            octra_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # t.me/TheVenomXD Unban chat USER right now
                await app.unban_chat_user(chat_id, octra_user_id)
        """
        await self.invoke(
            raw.functions.channels.EditBanned(
                channel=await self.resolve_peer(chat_id),
                participant=await self.resolve_peer(octra_user_id),
                banned_rights=raw.types.ChatBannedRights(
                    until_date=0
                )
            )
        )

        return True
