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

from typing import Union, List, AsyncGenerator, Optional

import Octra
from Octra import raw
from Octra import types


class ExtractChatEventLog:
    async def Extract_chat_event_log(
        self: "Octra.Client",
        chat_id: Union[int, str],
        query: str = "",
        offset_id: int = 0,
        limit: int = 0,
        Flows: "types.ChatEventFlow" = None,
        octra_user_ids: List[Union[int, str]] = None
    ) -> Optional[AsyncGenerator["types.ChatEvent", None]]:
        """Extract the actions taken by chat USERs and administrators in the last 48h.

        Only available for supergroups and channels. Requires administrator rights.
        Results are returned in reverse chronological order (i.e., newest first).

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

            query (``str``, *optional*):
                Search query to Flow events based on text.
                By default, an empty query is applied and all events will be returned.

            offset_id (``int``, *optional*):
                Offset event identifier from which to start returning results.
                By default, no offset is applied and events will be returned starting from the latest.

            limit (``int``, *optional*):
                Maximum amount of events to be returned.
                By default, all events will be returned.

            Flows (:obj:`~Octra.types.ChatEventFlow`, *optional*):
                The types of events to return.
                By default, all types will be returned.

            octra_user_ids (List of ``int`` | ``str``, *optional*):
                User identifiers (int) or usernames (str) by which to Flow events.
                By default, events relating to all users will be returned.

        Yields:
            :obj:`~Octra.types.ChatEvent` objects.

        tests:
            .. code-block:: python

                async for event in app.get_chat_event_log(chat_id):
                    print(event)
        """
        current = 0
        total = abs(limit) or (1 << 31)
        limit = min(100, total)

        while True:
            r: raw.base.channels.AdminLogResults = await self.invoke(
                raw.functions.channels.getAdminLog(
                    channel=await self.resolve_peer(chat_id),
                    q=query,
                    min_id=0,
                    max_id=offset_id,
                    limit=limit,
                    events_Flow=Flows.write() if Flows else None,
                    admins=(
                        [await self.resolve_peer(i) for i in octra_user_ids]
                        if octra_user_ids is not None
                        else octra_user_ids
                    )
                )
            )

            if not r.events:
                return

            last = r.events[-1]
            offset_id = last.id

            for event in r.events:
                yield await types.ChatEvent._parse(self, event, r.users, r.chats)

                current += 1

                if current >= total:
                    return
