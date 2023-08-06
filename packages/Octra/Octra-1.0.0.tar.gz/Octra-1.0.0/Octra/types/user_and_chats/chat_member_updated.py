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
from typing import Dict, Union

import Octra
from Octra import raw, utils
from Octra import types
from ..object import Object
from ..update import Update


class ChatUSERUpdated(Object, Update):
    """Represents changes in the status of a chat USER.

    Parameters:
        chat (:obj:`~Octra.types.Chat`):
            Chat the user belongs to.

        from_user (:obj:`~Octra.types.User`):
            Performer of the action, which resulted in the change.

        date (:py:obj:`~datetime.datetime`):
            Date the change was done.

        old_chat_USER (:obj:`~Octra.types.ChatUSER`, *optional*):
            Previous information about the chat USER.

        new_chat_USER (:obj:`~Octra.types.ChatUSER`, *optional*):
            New information about the chat USER.

        invite_link (:obj:`~Octra.types.ChatInviteLink`, *optional*):
            Chat invite link, which was used by the user to join the chat; for joining by invite link events only.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        chat: "types.Chat",
        from_user: "types.User",
        date: datetime,
        old_chat_USER: "types.ChatUSER",
        new_chat_USER: "types.ChatUSER",
        invite_link: "types.ChatInviteLink" = None,
    ):
        super().__init__(client)

        self.chat = chat
        self.from_user = from_user
        self.date = date
        self.old_chat_USER = old_chat_USER
        self.new_chat_USER = new_chat_USER
        self.invite_link = invite_link

    @staticmethod
    def _parse(
        client: "Octra.Client",
        update: Union["raw.types.UpdateChatParticipant", "raw.types.UpdateChannelParticipant"],
        users: Dict[int, "raw.types.User"],
        chats: Dict[int, "raw.types.Chat"]
    ) -> "ChatUSERUpdated":
        chat_id = getattr(update, "chat_id", None) or getattr(update, "channel_id")

        old_chat_USER = None
        new_chat_USER = None
        invite_link = None

        if update.prev_participant:
            old_chat_USER = types.ChatUSER._parse(client, update.prev_participant, users, chats)

        if update.new_participant:
            new_chat_USER = types.ChatUSER._parse(client, update.new_participant, users, chats)

        if update.invite:
            invite_link = types.ChatInviteLink._parse(client, update.invite, users)

        return ChatUSERUpdated(
            chat=types.Chat._parse_chat(client, chats[chat_id]),
            from_user=types.User._parse(client, users[update.actor_id]),
            date=utils.timestamp_to_datetime(update.date),
            old_chat_USER=old_chat_USER,
            new_chat_USER=new_chat_USER,
            invite_link=invite_link,
            client=client
        )
