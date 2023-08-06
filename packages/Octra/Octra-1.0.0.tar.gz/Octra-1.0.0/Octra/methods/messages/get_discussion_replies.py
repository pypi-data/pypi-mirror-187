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

from typing import Union, Optional, AsyncGenerator

import Octra
from Octra import types, raw


class ExtractDiscussionReplies:
    async def Extract_discussion_replies(
        self: "Octra.Client",
        chat_id: Union[int, str],
        message_id: int,
        limit: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Extract the message replies of a discussion thread.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

            message_id (``int``):
                Message id.

            limit (``int``, *optional*):
                Limits the number of messages to be retrieved.
                By default, no limit is applied and all messages are returned.

        Example:
            .. code-block:: python

                async for message in app.get_discussion_replies(chat_id, message_id):
                    print(message)
        """

        current = 0
        total = limit or (1 << 31) - 1
        limit = min(100, total)

        while True:
            r = await self.invoke(
                raw.functions.messages.getReplies(
                    peer=await self.resolve_peer(chat_id),
                    msg_id=message_id,
                    offset_id=0,
                    offset_date=0,
                    add_offset=current,
                    limit=limit,
                    max_id=0,
                    min_id=0,
                    hash=0
                )
            )

            users = {u.id: u for u in r.users}
            chats = {c.id: c for c in r.chats}
            messages = r.messages

            if not messages:
                return

            for message in messages:
                yield await types.Message._parse(self, message, users, chats, replies=0)

                current += 1

                if current >= total:
                    return
