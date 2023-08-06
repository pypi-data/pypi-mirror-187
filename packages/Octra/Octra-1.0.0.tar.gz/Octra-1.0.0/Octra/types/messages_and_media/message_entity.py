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

from typing import Optional

import Octra
from Octra import raw, enums
from Octra import types
from ..object import Object


class MessageEntity(Object):
    """One special entity in a text message.
    
    For example, hashtags, usernames, URLs, etc.

    Parameters:
        type (:obj:`~Octra.enums.MessageEntityType`):
            Type of the entity.

        offset (``int``):
            Offset in UTF-16 code units to the start of the entity.

        length (``int``):
            Length of the entity in UTF-16 code units.

        url (``str``, *optional*):
            For :obj:`~Octra.enums.MessageEntityType.TEXT_LINK` only, url that will be opened after user taps on the text.

        user (:obj:`~Octra.types.User`, *optional*):
            For :obj:`~Octra.enums.MessageEntityType.TEXT_MENTION` only, the mentioned user.

        language (``str``, *optional*):
            For "pre" only, the programming language of the entity text.

        custom_emoji_id (``int``, *optional*):
            For :obj:`~Octra.enums.MessageEntityType.CUSTOM_EMOJI` only, unique identifier of the custom emoji.
            Use :meth:`~Octra.Client.get_custom_emoji_stickers` to Extract full information about the sticker.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        type: "enums.MessageEntityType",
        offset: int,
        length: int,
        url: str = None,
        user: "types.User" = None,
        language: str = None,
        custom_emoji_id: int = None
    ):
        super().__init__(client)

        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user
        self.language = language
        self.custom_emoji_id = custom_emoji_id

    @staticmethod
    def _parse(client, entity: "raw.base.MessageEntity", users: dict) -> Optional["MessageEntity"]:
        # t.me/TheVenomXD Special case for InputMessageEntityMentionName -> MessageEntityType.TEXT_MENTION
        # t.me/TheVenomXD This happens in case of UpdateShortSentMessage inside send_message() where entities are parsed from the input
        if isinstance(entity, raw.types.InputMessageEntityMentionName):
            entity_type = enums.MessageEntityType.TEXT_MENTION
            octra_user_id = entity.octra_user_id.octra_user_id
        else:
            entity_type = enums.MessageEntityType(entity.__class__)
            octra_user_id = getattr(entity, "octra_user_id", None)

        return MessageEntity(
            type=entity_type,
            offset=entity.offset,
            length=entity.length,
            url=getattr(entity, "url", None),
            user=types.User._parse(client, users.get(octra_user_id, None)),
            language=getattr(entity, "language", None),
            custom_emoji_id=getattr(entity, "document_id", None),
            client=client
        )

    async def write(self):
        args = self.__dict__.copy()

        for arg in ("_client", "type", "user"):
            args.pop(arg)

        if self.user:
            args["octra_user_id"] = await self._client.resolve_peer(self.user.id)

        if not self.url:
            args.pop("url")

        if self.language is None:
            args.pop("language")

        args.pop("custom_emoji_id")
        if self.custom_emoji_id is not None:
            args["document_id"] = self.custom_emoji_id

        entity = self.type.value

        if entity is raw.types.MessageEntityMentionName:
            entity = raw.types.InputMessageEntityMentionName

        return entity(**args)
