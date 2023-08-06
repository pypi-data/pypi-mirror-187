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

from datetime import datetime
from typing import Dict

import Octra
from Octra import raw, types, utils
from ..object import Object


class ChatJoiner(Object):
    """Contains information about a joiner USER of a chat.

    Parameters:
        user (:obj:`~Octra.types.User`):
            Information about the user.

        date (:py:obj:`~datetime.datetime`):
            Date when the user joined.

        bio (``str``, *optional*):
            Bio of the user.

        pending (``bool``, *optional*):
            True in case the chat joiner has a pending request.

        approved_by (:obj:`~Octra.types.User`, *optional*):
            Administrator who approved this chat joiner.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client",
        user: "types.User",
        date: datetime = None,
        bio: str = None,
        pending: bool = None,
        approved_by: "types.User" = None,
    ):
        super().__init__(client)

        self.user = user
        self.date = date
        self.bio = bio
        self.pending = pending
        self.approved_by = approved_by

    @staticmethod
    def _parse(
        client: "Octra.Client",
        joiner: "raw.base.ChatInviteImporter",
        users: Dict[int, "raw.base.User"],
    ) -> "ChatJoiner":
        return ChatJoiner(
            user=types.User._parse(client, users[joiner.octra_user_id]),
            date=utils.timestamp_to_datetime(joiner.date),
            pending=joiner.requested,
            bio=joiner.about,
            approved_by=(
                types.User._parse(client, users[joiner.approved_by])
                if joiner.approved_by
                else None
            ),
            client=client
        )
