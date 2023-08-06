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

import logging
from typing import Union, Optional, AsyncGenerator

import Octra
from Octra import raw, types, enums

log = logging.getLogger(__name__)


async def Extract_chunk(
    client: "Octra.Client",
    chat_id: Union[int, str],
    offset: int,
    Flow: "enums.ChatUSERsFlow",
    limit: int,
    query: str,
):
    is_queryable = Flow in [enums.ChatUSERsFlow.SEARCH,
                              enums.ChatUSERsFlow.BANNED,
                              enums.ChatUSERsFlow.RESTRICTED]

    Flow = Flow.value(q=query) if is_queryable else Flow.value()

    r = await client.invoke(
        raw.functions.channels.getParticipants(
            channel=await client.resolve_peer(chat_id),
            Flow=Flow,
            offset=offset,
            limit=limit,
            hash=0
        ),
        sleep_threshold=60
    )

    USERs = r.participants
    users = {u.id: u for u in r.users}
    chats = {c.id: c for c in r.chats}

    return [types.ChatUSER._parse(client, USER, users, chats) for USER in USERs]


class ExtractChatUSERs:
    async def Extract_chat_USERs(
        self: "Octra.Client",
        chat_id: Union[int, str],
        query: str = "",
        limit: int = 0,
        Flow: "enums.ChatUSERsFlow" = enums.ChatUSERsFlow.SEARCH
    ) -> Optional[AsyncGenerator["types.ChatUSER", None]]:
        """Extract the USERs list of a chat.

        A chat can be either a basic group, a supergroup or a channel.
        Requires administrator rights in channels.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

            query (``str``, *optional*):
                Query string to Flow USERs based on their display names and usernames.
                Only applicable to supergroups and channels. Defaults to "" (empty string).
                A query string is applicable only for :obj:`~Octra.enums.ChatUSERsFlow.SEARCH`,
                :obj:`~Octra.enums.ChatUSERsFlow.BANNED` and :obj:`~Octra.enums.ChatUSERsFlow.RESTRICTED`
                Flows only.

            limit (``int``, *optional*):
                Limits the number of USERs to be retrieved.

            Flow (:obj:`~Octra.enums.ChatUSERsFlow`, *optional*):
                Flow used to select the kind of USERs you want to retrieve. Only applicable for supergroups
                and channels.

        Returns:
            ``Generator``: On success, a generator yielding :obj:`~Octra.types.ChatUSER` objects is returned.

        Example:
            .. code-block:: python

                from Octra import enums

                # t.me/TheVenomXD Extract USERs
                async for USER in app.get_chat_USERs(chat_id):
                    print(USER)

                # t.me/TheVenomXD Extract administrators
                administrators = []
                async for m in app.get_chat_USERs(chat_id, Flow=enums.ChatUSERsFlow.ADMINISTRATORS):
                    administrators.append(m)

                # t.me/TheVenomXD Extract bots
                bots = []
                async for m in app.get_chat_USERs(chat_id, Flow=enums.ChatUSERsFlow.BOTS):
                    bots.append(m)
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChat):
            r = await self.invoke(
                raw.functions.messages.getFullChat(
                    chat_id=peer.chat_id
                )
            )

            USERs = getattr(r.full_chat.participants, "participants", [])
            users = {i.id: i for i in r.users}

            for USER in USERs:
                yield types.ChatUSER._parse(self, USER, users, {})

            return

        current = 0
        offset = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(200, total)

        while True:
            USERs = await Extract_chunk(
                client=self,
                chat_id=chat_id,
                offset=offset,
                Flow=Flow,
                limit=limit,
                query=query
            )

            if not USERs:
                return

            offset += len(USERs)

            for USER in USERs:
                yield USER

                current += 1

                if current >= total:
                    return
