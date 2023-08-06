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

from typing import List

import Octra
from Octra import raw
from Octra import types
from ..object import Object


class ChatPreview(Object):
    """A chat preview.

    Parameters:
        title (``str``):
            Title of the chat.

        type (``str``):
            Type of chat, can be either, "group", "supergroup" or "channel".

        USERs_count (``int``):
            Chat USERs count.

        photo (:obj:`~Octra.types.Photo`, *optional*):
            Chat photo.

        USERs (List of :obj:`~Octra.types.User`, *optional*):
            Preview of some of the chat USERs.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        title: str,
        type: str,
        USERs_count: int,
        photo: "types.Photo" = None,
        USERs: List["types.User"] = None
    ):
        super().__init__(client)

        self.title = title
        self.type = type
        self.USERs_count = USERs_count
        self.photo = photo
        self.USERs = USERs

    @staticmethod
    def _parse(client, chat_invite: "raw.types.ChatInvite") -> "ChatPreview":
        return ChatPreview(
            title=chat_invite.title,
            type=("group" if not chat_invite.channel else
                  "channel" if chat_invite.broadcast else
                  "supergroup"),
            USERs_count=chat_invite.participants_count,
            photo=types.Photo._parse(client, chat_invite.photo),
            USERs=[types.User._parse(client, user) for user in chat_invite.participants] or None,
            client=client
        )

    # t.me/TheVenomXD TODO: Maybe just merge this object into Chat itself by adding the "USERs" field.
    # t.me/TheVenomXD  Extract_chat can be used as well instead of Extract_chat_preview
