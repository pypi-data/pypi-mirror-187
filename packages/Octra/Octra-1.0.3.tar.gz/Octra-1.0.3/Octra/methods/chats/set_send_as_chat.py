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


class SetSendAsChat:
    async def set_send_as_chat(
        self: "Octra.Client",
        chat_id: Union[int, str],
        send_as_chat_id: Union[int, str]
    ) -> bool:
        """Set the default "send_as" chat for a chat.

        Use :meth:`~Octra.Client.get_send_as_chats` to Extract all the "send_as" chats available for use.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

            send_as_chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the send_as chat.

        Returns:
            ``bool``: On success, true is returned

        Example:
            .. code-block:: python

                await app.set_send_as_chat(chat_id, send_as_chat_id)
        """
        return await self.invoke(
            raw.functions.messages.SaveDefaultSendAs(
                peer=await self.resolve_peer(chat_id),
                send_as=await self.resolve_peer(send_as_chat_id)
            )
        )
