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

from typing import Union, AsyncGenerator, Optional

import Octra
from Octra import types, raw, utils


class ExtractChatPhotos:
    async def Extract_chat_photos(
        self: "Octra.Client",
        chat_id: Union[int, str],
        limit: int = 0,
    ) -> Optional[AsyncGenerator["types.Photo", None]]:
        """Extract a chat or a user profile photos sequentially.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            limit (``int``, *optional*):
                Limits the number of profile photos to be retrieved.
                By default, no limit is applied and all profile photos are returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~Octra.types.Photo` objects.

        tests:
            .. code-block:: python

                async for photo in app.get_chat_photos("me"):
                    print(photo)
        """
        peer_id = await self.resolve_peer(chat_id)

        if isinstance(peer_id, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.getFullChannel(
                    channel=peer_id
                )
            )

            current = types.Photo._parse(self, r.full_chat.chat_photo) or []

            r = await utils.parse_messages(
                self,
                await self.invoke(
                    raw.functions.messages.Search(
                        peer=peer_id,
                        q="",
                        Flow=raw.types.InputMessagesFlowChatPhotos(),
                        min_date=0,
                        max_date=0,
                        offset_id=0,
                        add_offset=0,
                        limit=limit,
                        max_id=0,
                        min_id=0,
                        hash=0
                    )
                )
            )

            extra = [message.new_chat_photo for message in r]

            if extra:
                if current:
                    photos = ([current] + extra) if current.file_id != extra[0].file_id else extra
                else:
                    photos = extra
            else:
                if current:
                    photos = [current]
                else:
                    photos = []

            current = 0

            for photo in photos:
                yield photo

                current += 1

                if current >= limit:
                    return
        else:
            current = 0
            total = limit or (1 << 31)
            limit = min(100, total)
            offset = 0

            while True:
                r = await self.invoke(
                    raw.functions.photos.getUserPhotos(
                        octra_user_id=peer_id,
                        offset=offset,
                        max_id=0,
                        limit=limit
                    )
                )

                photos = [types.Photo._parse(self, photo) for photo in r.photos]

                if not photos:
                    return

                offset += len(photos)

                for photo in photos:
                    yield photo

                    current += 1

                    if current >= total:
                        return
