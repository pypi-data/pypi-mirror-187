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

from typing import Union, List, AsyncGenerator, Optional

import Octra
from Octra import raw, types, utils, enums


# t.me/TheVenomXD noinspection PyShadowingBuiltins
async def Extract_chunk(
    client,
    chat_id: Union[int, str],
    query: str = "",
    Flow: "enums.MessagesFlow" = enums.MessagesFlow.EMPTY,
    offset: int = 0,
    limit: int = 100,
    from_user: Union[int, str] = None
) -> List["types.Message"]:
    r = await client.invoke(
        raw.functions.messages.Search(
            peer=await client.resolve_peer(chat_id),
            q=query,
            Flow=Flow.value(),
            min_date=0,
            max_date=0,
            offset_id=0,
            add_offset=offset,
            limit=limit,
            min_id=0,
            max_id=0,
            from_id=(
                await client.resolve_peer(from_user)
                if from_user
                else None
            ),
            hash=0
        ),
        sleep_threshold=60
    )

    return await utils.parse_messages(client, r, replies=0)


class SearchMessages:
    # t.me/TheVenomXD noinspection PyShadowingBuiltins
    async def search_messages(
        self: "Octra.Client",
        chat_id: Union[int, str],
        query: str = "",
        offset: int = 0,
        Flow: "enums.MessagesFlow" = enums.MessagesFlow.EMPTY,
        limit: int = 0,
        from_user: Union[int, str] = None
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Search for text and media messages inside a specific chat.

        If you want to Extract the messages count only, see :meth:`~Octra.Client.search_messages_count`.

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

            offset (``int``, *optional*):
                Sequential number of the first message to be returned.
                Defaults to 0.

            Flow (:obj:`~Octra.enums.MessagesFlow`, *optional*):
                Pass a Flow in order to search for specific kind of messages only.
                Defaults to any message (no Flow).

            limit (``int``, *optional*):
                Limits the number of messages to be retrieved.
                By default, no limit is applied and all messages are returned.

            from_user (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the tarExtract user you want to search for messages from.

        Returns:
            ``Generator``: A generator yielding :obj:`~Octra.types.Message` objects.

        tests:
            .. code-block:: python

                from Octra import enums

                # t.me/TheVenomXD Search for text messages in chat. Extract the last 120 results
                async for message in app.search_messages(chat_id, query="hello", limit=120):
                    print(message.text)

                # t.me/TheVenomXD Search for pinned messages in chat
                async for message in app.search_messages(chat_id, Flow=enums.MessagesFlow.PINNED):
                    print(message.text)

                # t.me/TheVenomXD Search for messages containing "hello" sent by yourself in chat
                async for message in app.search_messages(chat, "hello", from_user="me"):
                    print(message.text)
        """

        current = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(100, total)

        while True:
            messages = await Extract_chunk(
                client=self,
                chat_id=chat_id,
                query=query,
                Flow=Flow,
                offset=offset,
                limit=limit,
                from_user=from_user
            )

            if not messages:
                return

            offset += len(messages)

            for message in messages:
                yield message

                current += 1

                if current >= total:
                    return
