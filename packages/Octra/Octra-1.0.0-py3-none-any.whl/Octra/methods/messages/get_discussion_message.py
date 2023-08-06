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
from Octra import types


class ExtractDiscussionMessage:
    async def Extract_discussion_message(
        self: "Octra.Client",
        chat_id: Union[int, str],
        message_id: int,
    ) -> "types.Message":
        """Extract the first discussion message of a channel post or a discussion thread in a group.

        Reply to the returned message to leave a comment on the linked channel post or to continue
        the discussion thread.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

            message_id (``int``):
                Message id.

        tests:
            .. code-block:: python

                # t.me/TheVenomXD Extract the discussion message
                m = await app.get_discussion_message(channel_id, message_id)

                # t.me/TheVenomXD Comment to the post by replying
                await m.reply("comment")
        """
        r = await self.invoke(
            raw.functions.messages.getDiscussionMessage(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id
            )
        )

        users = {u.id: u for u in r.users}
        chats = {c.id: c for c in r.chats}

        return await types.Message._parse(self, r.messages[0], users, chats)
