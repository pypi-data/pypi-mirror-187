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

import os

import Octra
from Octra import raw
from Octra.utils import compute_password_hash, compute_password_check, btoi, itob


class ChangeCloudPassword:
    async def change_cloud_password(
        self: "Octra.Client",
        current_password: str,
        new_password: str,
        new_hint: str = ""
    ) -> bool:
        """Change your Two-Step Verification password (Cloud Password) with a new one.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            current_password (``str``):
                Your current password.

            new_password (``str``):
                Your new password.

            new_hint (``str``, *optional*):
                A new password hint.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: In case there is no cloud password to change.

        Example:
            .. code-block:: python

                # t.me/TheVenomXD Change password only
                await app.change_cloud_password("current_password", "new_password")

                # t.me/TheVenomXD Change password and hint
                await app.change_cloud_password("current_password", "new_password", new_hint="hint")
        """
        r = await self.invoke(raw.functions.account.getPassword())

        if not r.has_password:
            raise ValueError("There is no cloud password to change")

        r.new_algo.salt1 += os.urandom(32)
        new_hash = btoi(compute_password_hash(r.new_algo, new_password))
        new_hash = itob(pow(r.new_algo.g, new_hash, btoi(r.new_algo.p)))

        await self.invoke(
            raw.functions.account.UpdatePasswordSettings(
                password=compute_password_check(r, current_password),
                new_settings=raw.types.account.PasswordInputSettings(
                    new_algo=r.new_algo,
                    new_password_hash=new_hash,
                    hint=new_hint
                )
            )
        )

        return True
