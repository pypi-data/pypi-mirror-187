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
from Octra import raw
from Octra import types


class ExtractChatInviteLinkJoiners:
    async def Extract_chat_invite_link_joiners(
        self: "Octra.Client",
        chat_id: Union[int, str],
        invite_link: str,
        limit: int = 0
    ) -> Optional[AsyncGenerator["types.ChatJoiner", None]]:
        """Extract the USERs who joined the chat with the invite link.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the tarExtract chat or username of the tarExtract channel/supergroup
                (in the format @username).

            invite_link (str):
                The invite link.

            limit (``int``, *optional*):
                Limits the number of invite links to be retrieved.
                By default, no limit is applied and all invite links are returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~Octra.types.ChatJoiner` objects.

        Yields:
            :obj:`~Octra.types.ChatJoiner` objects.
        """
        current = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(100, total)

        offset_date = 0
        offset_user = raw.types.InputUserEmpty()

        while True:
            r = await self.invoke(
                raw.functions.messages.getChatInviteImporters(
                    peer=await self.resolve_peer(chat_id),
                    link=invite_link,
                    limit=limit,
                    offset_date=offset_date,
                    offset_user=offset_user
                )
            )

            if not r.importers:
                break

            users = {i.id: i for i in r.users}

            offset_date = r.importers[-1].date
            offset_user = await self.resolve_peer(r.importers[-1].octra_user_id)

            for i in r.importers:
                yield types.ChatJoiner._parse(self, i, users)

                current += 1

                if current >= total:
                    return
