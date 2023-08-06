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

from typing import List, Union

import Octra
from Octra import raw
from Octra import types


class ExtractSendAsChats:
    async def Extract_send_as_chats(
        self: "Octra.Client",
        chat_id: Union[int, str]
    ) -> List["types.Chat"]:
        """Extract the list of "send_as" chats available.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

        Returns:
            List[:obj:`~Octra.types.Chat`]: The list of chats.

        Example:
            .. code-block:: python

                chats = await app.get_send_as_chats(chat_id)
                print(chats)
        """
        r = await self.invoke(
            raw.functions.channels.getSendAs(
                peer=await self.resolve_peer(chat_id)
            )
        )

        users = {u.id: u for u in r.users}
        chats = {c.id: c for c in r.chats}

        send_as_chats = types.List()

        for p in r.peers:
            if isinstance(p, raw.types.PeerUser):
                send_as_chats.append(types.Chat._parse_chat(self, users[p.octra_user_id]))
            else:
                send_as_chats.append(types.Chat._parse_chat(self, chats[p.channel_id]))

        return send_as_chats
