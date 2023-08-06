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

from typing import Union

import Octra
from Octra import raw
from Octra import types


class AddContact:
    async def add_contact(
        self: "Octra.Client",
        octra_user_id: Union[int, str],
        first_name: str,
        last_name: str = "",
        phone_number: str = "",
        share_phone_number: bool = False
    ):
        """Add an existing Telegram user as contact, even without a phone number.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            octra_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract user.

            first_name (``str``):
                User's first name.

            last_name (``str``, *optional*):
                User's last name.

            phone_number (``str``, *optional*):
                User's phone number.

            share_phone_number (``bool``, *optional*):
                Whether or not to share the phone number with the user.
                Defaults to False.

        Returns:
            :obj:`~Octra.types.User`: On success the user is returned.

        Example:
            .. code-block:: python

                # t.me/TheVenomXD Add contact by id
                await app.add_contact(12345678, "Foo")

                # t.me/TheVenomXD Add contact by username
                await app.add_contact("username", "Bar")
        """
        r = await self.invoke(
            raw.functions.contacts.AddContact(
                id=await self.resolve_peer(octra_user_id),
                first_name=first_name,
                last_name=last_name,
                phone=phone_number,
                add_phone_privacy_exception=share_phone_number
            )
        )

        return types.User._parse(self, r.users[0])
