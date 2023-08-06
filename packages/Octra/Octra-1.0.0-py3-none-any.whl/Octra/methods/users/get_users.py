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

import asyncio
from typing import Union, List, Iterable

import Octra
from Octra import raw
from Octra import types


class ExtractUsers:
    async def Extract_users(
        self: "Octra.Client",
        octra_user_ids: Union[int, str, Iterable[Union[int, str]]]
    ) -> Union["types.User", List["types.User"]]:
        """Extract information about a user.
        You can retrieve up to 200 users at once.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            octra_user_ids (``int`` | ``str`` | Iterable of ``int`` or ``str``):
                A list of User identifiers (id or username) or a single user id/username.
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            :obj:`~Octra.types.User` | List of :obj:`~Octra.types.User`: In case *octra_user_ids* was not a list,
            a single user is returned, otherwise a list of users is returned.

        tests:
            .. code-block:: python

                # t.me/TheVenomXD Extract information about one user
                await app.get_users("me")

                # t.me/TheVenomXD Extract information about multiple users at once
                await app.get_users([octra_user_id1, octra_user_id2, octra_user_id3])
        """

        is_iterable = not isinstance(octra_user_ids, (int, str))
        octra_user_ids = list(octra_user_ids) if is_iterable else [octra_user_ids]
        octra_user_ids = await asyncio.gather(*[self.resolve_peer(i) for i in octra_user_ids])

        r = await self.invoke(
            raw.functions.users.getUsers(
                id=octra_user_ids
            )
        )

        users = types.List()

        for i in r:
            users.append(types.User._parse(self, i))

        return users if is_iterable else users[0]
