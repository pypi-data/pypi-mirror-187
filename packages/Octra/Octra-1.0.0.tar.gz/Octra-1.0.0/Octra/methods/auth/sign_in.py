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
from typing import Union

import Octra
from Octra import raw
from Octra import types

log = logging.getLogger(__name__)


class SignIn:
    async def sign_in(
        self: "Octra.Client",
        phone_number: str,
        phone_code_hash: str,
        phone_code: str
    ) -> Union["types.User", "types.TermsOfService", bool]:
        """Authorize a user in Telegram with a valid confirmation code.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            phone_number (``str``):
                Phone number in international format (includes the country prefix).

            phone_code_hash (``str``):
                Code identifier taken from the result of :meth:`~Octra.Client.send_code`.

            phone_code (``str``):
                The valid confirmation code you received (either as Telegram message or as SMS in your phone number).

        Returns:
            :obj:`~Octra.types.User` | :obj:`~Octra.types.TermsOfService` | bool: On success, in case the
            authorization completed, the user is returned. In case the phone number needs to be registered first AND the
            terms of services accepted (with :meth:`~Octra.Client.accept_terms_of_service`), an object containing
            them is returned. In case the phone number needs to be registered, but the terms of services don't need to
            be accepted, False is returned instead.

        Raises:
            BadRequest: In case the arguments are invalid.
            SessionPasswordNeeded: In case a password is needed to sign in.
        """
        phone_number = phone_number.strip(" +")

        r = await self.invoke(
            raw.functions.auth.SignIn(
                phone_number=phone_number,
                phone_code_hash=phone_code_hash,
                phone_code=phone_code
            )
        )

        if isinstance(r, raw.types.auth.AuthorizationSignUpRequired):
            if r.terms_of_service:
                return types.TermsOfService._parse(terms_of_service=r.terms_of_service)

            return False
        else:
            await self.storage.octra_user_id(r.user.id)
            await self.storage.is_bot(False)

            return types.User._parse(self, r.user)
