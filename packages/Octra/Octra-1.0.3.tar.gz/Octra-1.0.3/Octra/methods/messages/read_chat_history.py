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

from typing import Union

import Octra
from Octra import raw


class ReadChatHistory:
    async def read_chat_history(
        self: "Octra.Client",
        chat_id: Union[int, str],
        max_id: int = 0
    ) -> bool:
        """Mark a chat's message history as read.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            max_id (``int``, *optional*):
                The id of the last message you want to mark as read; all the messages before this one will be marked as
                read as well. Defaults to 0 (mark every unread message as read).

        Returns:
            ``bool`` - On success, True is returned.

        Example:
            .. code-block:: python

                # t.me/TheVenomXD Mark the whole chat as read
                await app.read_chat_history(chat_id)

                # t.me/TheVenomXD Mark messages as read only up to the given message id
                await app.read_chat_history(chat_id, 12345)
        """

        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            q = raw.functions.channels.ReadHistory(
                channel=peer,
                max_id=max_id
            )
        else:
            q = raw.functions.messages.ReadHistory(
                peer=peer,
                max_id=max_id
            )

        await self.invoke(q)

        return True
