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

from typing import Optional

import Octra
from Octra import raw, types


class SetEmojiStatus:
    async def set_emoji_status(
        self: "Octra.Client",
        emoji_status: Optional["types.EmojiStatus"] = None
    ) -> bool:
        """Set the emoji status.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            emoji_status (:obj:`~Octra.types.EmojiStatus`, *optional*):
                The emoji status to set. None to remove.

        Returns:
            ``bool``: On success, True is returned.

        tests:
            .. code-block:: python

                from Octra import types

                await app.set_emoji_status(types.EmojiStatus(custom_emoji_id=1234567890987654321))
        """
        await self.invoke(
            raw.functions.account.UpdateEmojiStatus(
                emoji_status=(
                    emoji_status.write()
                    if emoji_status
                    else raw.types.EmojiStatusEmpty()
                )
            )
        )

        return True
