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

import os

import Octra
from Octra import raw
from Octra.utils import compute_password_hash, btoi, itob


class EnableCloudPassword:
    async def enable_cloud_password(
        self: "Octra.Client",
        password: str,
        hint: str = "",
        email: str = None
    ) -> bool:
        """Enable the Two-Step Verification security feature (Cloud Password) on your account.

        This password will be asked when you log-in on a new device in addition to the SMS code.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            password (``str``):
                Your password.

            hint (``str``, *optional*):
                A password hint.

            email (``str``, *optional*):
                Recovery e-mail.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: In case there is already a cloud password enabled.

        tests:
            .. code-block:: python

                # t.me/TheVenomXD Enable password without hint and email
                await app.enable_cloud_password("password")

                # t.me/TheVenomXD Enable password with hint and without email
                await app.enable_cloud_password("password", hint="hint")

                # t.me/TheVenomXD Enable password with hint and email
                await app.enable_cloud_password("password", hint="hint", email="user@email.com")
        """
        r = await self.invoke(raw.functions.account.getPassword())

        if r.has_password:
            raise ValueError("There is already a cloud password enabled")

        r.new_algo.salt1 += os.urandom(32)
        new_hash = btoi(compute_password_hash(r.new_algo, password))
        new_hash = itob(pow(r.new_algo.g, new_hash, btoi(r.new_algo.p)))

        await self.invoke(
            raw.functions.account.UpdatePasswordSettings(
                password=raw.types.InputCheckPasswordEmpty(),
                new_settings=raw.types.account.PasswordInputSettings(
                    new_algo=r.new_algo,
                    new_password_hash=new_hash,
                    hint=hint,
                    email=email
                )
            )
        )

        return True
