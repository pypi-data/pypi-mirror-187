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


class ExtractChatAdminInviteLinks:
    async def Extract_chat_admin_invite_links(
        self: "Octra.Client",
        chat_id: Union[int, str],
        admin_id: Union[int, str],
        revoked: bool = False,
        limit: int = 0,
    ) -> Optional[AsyncGenerator["types.ChatInviteLink", None]]:
        """Extract the invite links created by an administrator in a chat.

        .. note::

            As an administrator you can only Extract your own links you have exported.
            As the chat or channel owner you can Extract everyones links.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the tarExtract chat or username of the tarExtract channel/supergroup
                (in the format @username).

            admin_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract user.
                For you yourself you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            revoked (``bool``, *optional*):
                True, if you want to Extract revoked links instead.
                Defaults to False (Extract active links only).

            limit (``int``, *optional*):
                Limits the number of invite links to be retrieved.
                By default, no limit is applied and all invite links are returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~Octra.types.ChatInviteLink` objects.

        Yields:
            :obj:`~Octra.types.ChatInviteLink` objects.
        """
        current = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(100, total)

        offset_date = None
        offset_link = None

        while True:
            r = await self.invoke(
                raw.functions.messages.getExportedChatInvites(
                    peer=await self.resolve_peer(chat_id),
                    admin_id=await self.resolve_peer(admin_id),
                    limit=limit,
                    revoked=revoked,
                    offset_date=offset_date,
                    offset_link=offset_link
                )
            )

            if not r.invites:
                break

            users = {i.id: i for i in r.users}

            offset_date = r.invites[-1].date
            offset_link = r.invites[-1].link

            for i in r.invites:
                yield types.ChatInviteLink._parse(self, i, users)

                current += 1

                if current >= total:
                    return
