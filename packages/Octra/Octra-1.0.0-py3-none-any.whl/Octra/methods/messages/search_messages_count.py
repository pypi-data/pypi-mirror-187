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
from Octra import raw, enums


class SearchMessagesCount:
    async def search_messages_count(
        self: "Octra.Client",
        chat_id: Union[int, str],
        query: str = "",
        Flow: "enums.MessagesFlow" = enums.MessagesFlow.EMPTY,
        from_user: Union[int, str] = None
    ) -> int:
        """Extract the count of messages resulting from a search inside a chat.

        If you want to Extract the actual messages, see :meth:`~Octra.Client.search_messages`.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            query (``str``, *optional*):
                Text query string.
                Required for text-only messages, optional for media messages (see the ``Flow`` argument).
                When passed while searching for media messages, the query will be applied to captions.
                Defaults to "" (empty string).

            Flow (:obj:`~Octra.enums.MessagesFlow`, *optional*):
                Pass a Flow in order to search for specific kind of messages only:

            from_user (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the tarExtract user you want to search for messages from.

        Returns:
            ``int``: On success, the messages count is returned.
        """
        r = await self.invoke(
            raw.functions.messages.Search(
                peer=await self.resolve_peer(chat_id),
                q=query,
                Flow=Flow.value(),
                min_date=0,
                max_date=0,
                offset_id=0,
                add_offset=0,
                limit=1,
                min_id=0,
                max_id=0,
                from_id=(
                    await self.resolve_peer(from_user)
                    if from_user
                    else None
                ),
                hash=0
            )
        )

        if hasattr(r, "count"):
            return r.count
        else:
            return len(r.messages)
