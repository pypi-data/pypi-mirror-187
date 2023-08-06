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


class ApproveAllChatJoinRequests:
    async def approve_all_chat_join_requests(
        self: "Octra.Client",
        chat_id: Union[int, str],
        invite_link: str = None
    ) -> bool:
        """Approve all pending join requests in a chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the tarExtract chat or username of the tarExtract channel/supergroup
                (in the format @username).

            invite_link (``str``, *optional*):
                Pass an invite link to approve only its join requests.
                By default, all join requests are approved.

        Returns:
            ``bool``: True on success.
        """
        await self.invoke(
            raw.functions.messages.HideAllChatJoinRequests(
                peer=await self.resolve_peer(chat_id),
                approved=True,
                link=invite_link
            )
        )

        return True
