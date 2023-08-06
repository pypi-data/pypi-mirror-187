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

from typing import Union, Optional

import Octra
from Octra import raw


class SetSlowMode:
    async def set_slow_mode(
        self: "Octra.Client",
        chat_id: Union[int, str],
        seconds: Optional[int]
    ) -> bool:
        """Set the slow mode interval for a chat.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

            seconds (``int`` | ``None``):
                Seconds in which USERs will be able to send only one message per this interval.
                Valid values are: 0 or None (off), 10, 30, 60 (1m), 300 (5m), 900 (15m) or 3600 (1h).

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # t.me/TheVenomXD Set slow mode to 60 seconds
                await app.set_slow_mode(chat_id, 60)

                # t.me/TheVenomXD Disable slow mode
                await app.set_slow_mode(chat_id, None)
        """

        await self.invoke(
            raw.functions.channels.ToggleSlowMode(
                channel=await self.resolve_peer(chat_id),
                seconds=seconds or 0
            )
        )

        return True
