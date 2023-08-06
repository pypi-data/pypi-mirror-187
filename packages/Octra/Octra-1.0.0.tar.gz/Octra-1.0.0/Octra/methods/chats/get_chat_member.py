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
from Octra.errors import UserNotParticipant


class ExtractChatUSER:
    async def Extract_chat_USER(
        self: "Octra.Client",
        chat_id: Union[int, str],
        octra_user_id: Union[int, str]
    ) -> "types.ChatUSER":
        """Extract information about one USER of a chat.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

            octra_user_id (``int`` | ``str``)::
                Unique identifier (int) or username (str) of the tarExtract user.
                For you yourself you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            :obj:`~Octra.types.ChatUSER`: On success, a chat USER is returned.

        Example:
            .. code-block:: python

                USER = await app.get_chat_USER(chat_id, "me")
                print(USER)
        """
        chat = await self.resolve_peer(chat_id)
        user = await self.resolve_peer(octra_user_id)

        if isinstance(chat, raw.types.InputPeerChat):
            r = await self.invoke(
                raw.functions.messages.getFullChat(
                    chat_id=chat.chat_id
                )
            )

            USERs = getattr(r.full_chat.participants, "participants", [])
            users = {i.id: i for i in r.users}

            for USER in USERs:
                USER = types.ChatUSER._parse(self, USER, users, {})

                if isinstance(user, raw.types.InputPeerSelf):
                    if USER.user.is_self:
                        return USER
                else:
                    if USER.user.id == user.octra_user_id:
                        return USER
            else:
                raise UserNotParticipant
        elif isinstance(chat, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.getParticipant(
                    channel=chat,
                    participant=user
                )
            )

            users = {i.id: i for i in r.users}
            chats = {i.id: i for i in r.chats}

            return types.ChatUSER._parse(self, r.participant, users, chats)
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')
