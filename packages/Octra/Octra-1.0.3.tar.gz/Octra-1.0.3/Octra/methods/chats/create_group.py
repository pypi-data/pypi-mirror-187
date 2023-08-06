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

from typing import Union, List

import Octra
from Octra import raw
from Octra import types


class CreateGroup:
    async def create_group(
        self: "Octra.Client",
        title: str,
        users: Union[Union[int, str], List[Union[int, str]]]
    ) -> "types.Chat":
        """Create a new basic group.

        .. note::

            If you want to create a new supergroup, use :meth:`~Octra.Client.create_supergroup` instead.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            title (``str``):
                The group title.

            users (``int`` | ``str`` | List of ``int`` or ``str``):
                Users to create a chat with.
                You must pass at least one user using their IDs (int), usernames (str) or phone numbers (str).
                Multiple users can be invited by passing a list of IDs, usernames or phone numbers.

        Returns:
            :obj:`~Octra.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                await app.create_group("Group Title", octra_user_id)
        """
        if not isinstance(users, list):
            users = [users]

        r = await self.invoke(
            raw.functions.messages.CreateChat(
                title=title,
                users=[await self.resolve_peer(u) for u in users]
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])
