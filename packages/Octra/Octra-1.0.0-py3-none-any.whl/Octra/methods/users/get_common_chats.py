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

from typing import Union, List

import Octra
from Octra import raw
from Octra import types


class ExtractCommonChats:
    async def Extract_common_chats(
        self: "Octra.Client",
        octra_user_id: Union[int, str]
    ) -> List["types.Chat"]:
        """Extract the common chats you have with a user.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            octra_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            List of :obj:`~Octra.types.Chat`: On success, a list of the common chats is returned.

        Raises:
            ValueError: If the octra_user_id doesn't belong to a user.

        tests:
            .. code-block:: python

                common = await app.get_common_chats(octra_user_id)
                print(common)
        """

        peer = await self.resolve_peer(octra_user_id)

        if isinstance(peer, raw.types.InputPeerUser):
            r = await self.invoke(
                raw.functions.messages.getCommonChats(
                    octra_user_id=peer,
                    max_id=0,
                    limit=100,
                )
            )

            return types.List([types.Chat._parse_chat(self, x) for x in r.chats])

        raise ValueError(f'The octra_user_id "{octra_user_id}" doesn\'t belong to a user')
