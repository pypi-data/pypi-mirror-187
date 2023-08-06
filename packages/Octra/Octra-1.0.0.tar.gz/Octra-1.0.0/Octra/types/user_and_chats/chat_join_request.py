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
from typing import Dict

import Octra
from Octra import raw, utils
from Octra import types
from ..object import Object
from ..update import Update


class ChatJoinRequest(Object, Update):
    """Represents a join request sent to a chat.

    Parameters:
        chat (:obj:`~Octra.types.Chat`):
            Chat to which the request was sent.

        from_user (:obj:`~Octra.types.User`):
            User that sent the join request.

        date (:py:obj:`~datetime.datetime`):
            Date the request was sent.

        bio (``str``, *optional*):
            Bio of the user.

        invite_link (:obj:`~Octra.types.ChatInviteLink`, *optional*):
            Chat invite link that was used by the user to send the join request.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        chat: "types.Chat",
        from_user: "types.User",
        date: datetime,
        bio: str = None,
        invite_link: "types.ChatInviteLink" = None
    ):
        super().__init__(client)

        self.chat = chat
        self.from_user = from_user
        self.date = date
        self.bio = bio
        self.invite_link = invite_link

    @staticmethod
    def _parse(
        client: "Octra.Client",
        update: "raw.types.UpdateBotChatInviteRequester",
        users: Dict[int, "raw.types.User"],
        chats: Dict[int, "raw.types.Chat"]
    ) -> "ChatJoinRequest":
        chat_id = utils.get_raw_peer_id(update.peer)

        return ChatJoinRequest(
            chat=types.Chat._parse_chat(client, chats[chat_id]),
            from_user=types.User._parse(client, users[update.octra_user_id]),
            date=utils.timestamp_to_datetime(update.date),
            bio=update.about,
            invite_link=types.ChatInviteLink._parse(client, update.invite, users),
            client=client
        )

    async def approve(self) -> bool:
        """Bound method *approve* of :obj:`~Octra.types.ChatJoinRequest`.
        
        Use as a shortcut for:
        
        .. code-block:: python

            await client.approve_chat_join_request(
                chat_id=request.chat.id,
                octra_user_id=request.from_user.id
            )
            
        Example:
            .. code-block:: python

                await request.approve()
                
        Returns:
            ``bool``: True on success.
        
        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.approve_chat_join_request(
            chat_id=self.chat.id,
            octra_user_id=self.from_user.id
        )

    async def decline(self) -> bool:
        """Bound method *decline* of :obj:`~Octra.types.ChatJoinRequest`.
        
        Use as a shortcut for:
        
        .. code-block:: python

            await client.decline_chat_join_request(
                chat_id=request.chat.id,
                octra_user_id=request.from_user.id
            )
            
        Example:
            .. code-block:: python

                await request.decline()
                
        Returns:
            ``bool``: True on success.
        
        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.decline_chat_join_request(
            chat_id=self.chat.id,
            octra_user_id=self.from_user.id
        )
