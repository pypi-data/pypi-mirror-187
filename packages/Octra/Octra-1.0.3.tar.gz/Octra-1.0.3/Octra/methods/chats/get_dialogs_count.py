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


class ExtractDialogsCount:
    async def Extract_dialogs_count(
        self: "Octra.Client",
        pinned_only: bool = False
    ) -> int:
        """Extract the total count of your dialogs.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            pinned_only (``bool``, *optional*):
                Pass True if you want to count only pinned dialogs.
                Defaults to False.

        Returns:
            ``int``: On success, the dialogs count is returned.

        Example:
            .. code-block:: python

                count = await app.get_dialogs_count()
                print(count)
        """

        if pinned_only:
            return len((await self.invoke(raw.functions.messages.getPinnedDialogs(folder_id=0))).dialogs)
        else:
            r = await self.invoke(
                raw.functions.messages.getDialogs(
                    offset_date=0,
                    offset_id=0,
                    offset_peer=raw.types.InputPeerEmpty(),
                    limit=1,
                    hash=0
                )
            )

            if isinstance(r, raw.types.messages.Dialogs):
                return len(r.dialogs)
            else:
                return r.count
