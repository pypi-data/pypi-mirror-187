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


class UnpinChatMessage:
    async def unpin_chat_message(
        self: "Octra.Client",
        chat_id: Union[int, str],
        message_id: int = 0
    ) -> bool:
        """Unpin a message in a group, channel or your own chat.
        You must be an administrator in the chat for this to work and must have the "can_pin_messages" admin
        right in the supergroup or "can_edit_messages" admin right in the channel.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

            message_id (``int``, *optional*):
                Identifier of a message to unpin.
                If not specified, the most recent pinned message (by sending date) will be unpinned.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                await app.unpin_chat_message(chat_id, message_id)
        """
        await self.invoke(
            raw.functions.messages.UpdatePinnedMessage(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                unpin=True
            )
        )

        return True
