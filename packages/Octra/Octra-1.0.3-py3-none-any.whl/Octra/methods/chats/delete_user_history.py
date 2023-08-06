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

from typing import Union

import Octra
from Octra import raw


class DeleteUserHistory:
    async def delete_user_history(
        self: "Octra.Client",
        chat_id: Union[int, str],
        octra_user_id: Union[int, str],
    ) -> bool:
        """Delete all messages sent by a certain user in a supergroup.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

            octra_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the user whose messages will be deleted.

        Returns:
            ``bool``: True on success, False otherwise.
        """

        r = await self.invoke(
            raw.functions.channels.DeleteParticipantHistory(
                channel=await self.resolve_peer(chat_id),
                participant=await self.resolve_peer(octra_user_id)
            )
        )

        # t.me/TheVenomXD Deleting messages you don't have right onto won't raise any error.
        # t.me/TheVenomXD Check for pts_count, which is 0 in case deletes fail.
        return bool(r.pts_count)
