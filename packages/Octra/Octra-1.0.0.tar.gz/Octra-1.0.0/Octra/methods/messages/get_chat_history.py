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

from datetime import datetime
from typing import Union, Optional, AsyncGenerator

import Octra
from Octra import types, raw, utils


async def Extract_chunk(
    *,
    client: "Octra.Client",
    chat_id: Union[int, str],
    limit: int = 0,
    offset: int = 0,
    from_message_id: int = 0,
    from_date: datetime = utils.zero_datetime()
):
    messages = await client.invoke(
        raw.functions.messages.getHistory(
            peer=await client.resolve_peer(chat_id),
            offset_id=from_message_id,
            offset_date=utils.datetime_to_timestamp(from_date),
            add_offset=offset,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ),
        sleep_threshold=60
    )

    return await utils.parse_messages(client, messages, replies=0)


class ExtractChatHistory:
    async def Extract_chat_history(
        self: "Octra.Client",
        chat_id: Union[int, str],
        limit: int = 0,
        offset: int = 0,
        offset_id: int = 0,
        offset_date: datetime = utils.zero_datetime()
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Extract messages from a chat history.

        The messages are returned in reverse chronological order.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            limit (``int``, *optional*):
                Limits the number of messages to be retrieved.
                By default, no limit is applied and all messages are returned.

            offset (``int``, *optional*):
                Sequential number of the first message to be returned..
                Negative values are also accepted and become useful in case you set offset_id or offset_date.

            offset_id (``int``, *optional*):
                Identifier of the first message to be returned.

            offset_date (:py:obj:`~datetime.datetime`, *optional*):
                Pass a date as offset to retrieve only older messages starting from that date.

        Returns:
            ``Generator``: A generator yielding :obj:`~Octra.types.Message` objects.

        Example:
            .. code-block:: python

                async for message in app.get_chat_history(chat_id):
                    print(message.text)
        """
        current = 0
        total = limit or (1 << 31) - 1
        limit = min(100, total)

        while True:
            messages = await Extract_chunk(
                client=self,
                chat_id=chat_id,
                limit=limit,
                offset=offset,
                from_message_id=offset_id,
                from_date=offset_date
            )

            if not messages:
                return

            offset_id = messages[-1].id

            for message in messages:
                yield message

                current += 1

                if current >= total:
                    return
