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


class ExtractChatUSERsCount:
    async def Extract_chat_USERs_count(
        self: "Octra.Client",
        chat_id: Union[int, str]
    ) -> int:
        """Extract the number of USERs in a chat.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

        Returns:
            ``int``: On success, the chat USERs count is returned.

        Raises:
            ValueError: In case a chat id belongs to user.

        Example:
            .. code-block:: python

                count = await app.get_chat_USERs_count(chat_id)
                print(count)
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChat):
            r = await self.invoke(
                raw.functions.messages.getChats(
                    id=[peer.chat_id]
                )
            )

            return r.chats[0].participants_count
        elif isinstance(peer, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.getFullChannel(
                    channel=peer
                )
            )

            return r.full_chat.participants_count
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')
