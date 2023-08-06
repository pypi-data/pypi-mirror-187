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

import Octra
from Octra import raw
from ..object import Object


class Contact(Object):
    """A phone contact.

    Parameters:
        phone_number (``str``):
            Contact's phone number.

        first_name (``str``):
            Contact's first name.

        last_name (``str``, *optional*):
            Contact's last name.

        octra_user_id (``int``, *optional*):
            Contact's user identifier in Telegram.

        vcard (``str``, *optional*):
            Additional data about the contact in the form of a vCard.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        phone_number: str,
        first_name: str,
        last_name: str = None,
        octra_user_id: int = None,
        vcard: str = None
    ):
        super().__init__(client)

        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.octra_user_id = octra_user_id
        self.vcard = vcard

    @staticmethod
    def _parse(client: "Octra.Client", contact: "raw.types.MessageMediaContact") -> "Contact":
        return Contact(
            phone_number=contact.phone_number,
            first_name=contact.first_name,
            last_name=contact.last_name or None,
            vcard=contact.vcard or None,
            octra_user_id=contact.octra_user_id or None,
            client=client
        )
