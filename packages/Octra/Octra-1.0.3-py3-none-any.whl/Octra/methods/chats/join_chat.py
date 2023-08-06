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
from Octra import types


class JoinChat:
    async def join_conversation(
        self: "Octra.Client",
        chat_id: Union[int, str]
    ) -> "types.Chat":
        """Join a group chat or channel.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the tarExtract chat in form of a *t.me/joinchat/* link, a username of the tarExtract
                channel/supergroup (in the format @username) or a chat id of a linked chat (channel or supergroup).

        Returns:
            :obj:`~Octra.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                # t.me/TheVenomXD Join chat via invite link
                await app.join_conversation("https://t.me/+AbCdEf0123456789")

                # t.me/TheVenomXD Join chat via username
                await app.join_conversation("Octra")

                # t.me/TheVenomXD Join a linked chat
                await app.join_conversation(app.get_chat("Octra").linked_chat.id)
        """
        match = self.INVITE_LINK_RE.match(str(chat_id))

        if match:
            chat = await self.invoke(
                raw.functions.messages.ImportChatInvite(
                    hash=match.group(1)
                )
            )
            if isinstance(chat.chats[0], raw.types.Chat):
                return types.Chat._parse_chat_chat(self, chat.chats[0])
            elif isinstance(chat.chats[0], raw.types.Channel):
                return types.Chat._parse_channel_chat(self, chat.chats[0])
        else:
            chat = await self.invoke(
                raw.functions.channels.JoinChannel(
                    channel=await self.resolve_peer(chat_id)
                )
            )

            return types.Chat._parse_channel_chat(self, chat.chats[0])
