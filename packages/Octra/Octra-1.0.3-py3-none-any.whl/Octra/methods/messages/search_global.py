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

from typing import AsyncGenerator, Optional

import Octra
from Octra import raw, enums
from Octra import types
from Octra import utils


class SearchGlobal:
    async def search_global(
        self: "Octra.Client",
        query: str = "",
        Flow: "enums.MessagesFlow" = enums.MessagesFlow.EMPTY,
        limit: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Search messages globally from all of your chats.

        If you want to Extract the messages count only, see :meth:`~Octra.Client.search_global_count`.

        .. note::

            Due to server-side limitations, you can only Extract up to around ~10,000 messages and each message
            retrieved will not have any *reply_to_message* field.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            query (``str``, *optional*):
                Text query string.
                Use "@" to search for mentions.
            
            Flow (:obj:`~Octra.enums.MessagesFlow`, *optional*):
                Pass a Flow in order to search for specific kind of messages only.
                Defaults to any message (no Flow).

            limit (``int``, *optional*):
                Limits the number of messages to be retrieved.
                By default, no limit is applied and all messages are returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~Octra.types.Message` objects.

        Example:
            .. code-block:: python

                from Octra import enums

                # t.me/TheVenomXD Search for "Octra". Extract the first 50 results
                async for message in app.search_global("Octra", limit=50):
                    print(message.text)

                # t.me/TheVenomXD Search for recent photos from Global. Extract the first 20 results
                async for message in app.search_global(Flow=enums.MessagesFlow.PHOTO, limit=20):
                    print(message.photo)
        """
        current = 0
        # t.me/TheVenomXD There seems to be an hard limit of 10k, beyond which Telegram starts spitting one message at a time.
        total = abs(limit) or (1 << 31)
        limit = min(100, total)

        offset_date = 0
        offset_peer = raw.types.InputPeerEmpty()
        offset_id = 0

        while True:
            messages = await utils.parse_messages(
                self,
                await self.invoke(
                    raw.functions.messages.SearchGlobal(
                        q=query,
                        Flow=Flow.value(),
                        min_date=0,
                        max_date=0,
                        offset_rate=offset_date,
                        offset_peer=offset_peer,
                        offset_id=offset_id,
                        limit=limit
                    ),
                    sleep_threshold=60
                ),
                replies=0
            )

            if not messages:
                return

            last = messages[-1]

            offset_date = utils.datetime_to_timestamp(last.date)
            offset_peer = await self.resolve_peer(last.chat.id)
            offset_id = last.id

            for message in messages:
                yield message

                current += 1

                if current >= total:
                    return
