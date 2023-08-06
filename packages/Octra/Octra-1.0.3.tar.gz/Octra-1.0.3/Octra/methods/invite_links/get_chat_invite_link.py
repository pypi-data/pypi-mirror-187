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
from Octra import types


class ExtractChatInviteLink:
    async def Extract_chat_invite_link(
        self: "Octra.Client",
        chat_id: Union[int, str],
        invite_link: str,
    ) -> "types.ChatInviteLink":
        """Extract detailed information about a chat invite link.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the tarExtract chat or username of the tarExtract channel/supergroup
                (in the format @username).

            invite_link (str):
                The invite link.

        Returns:
            :obj:`~Octra.types.ChatInviteLink`: On success, the invite link is returned.
        """
        r = await self.invoke(
            raw.functions.messages.getExportedChatInvite(
                peer=await self.resolve_peer(chat_id),
                link=invite_link
            )
        )

        users = {i.id: i for i in r.users}

        return types.ChatInviteLink._parse(self, r.invite, users)
