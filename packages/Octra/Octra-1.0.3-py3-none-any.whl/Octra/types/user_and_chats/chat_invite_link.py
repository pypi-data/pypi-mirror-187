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

from datetime import datetime
from typing import Dict
from typing import Optional

import Octra
from Octra import raw, utils
from Octra import types
from ..object import Object


class ChatInviteLink(Object):
    """An invite link for a chat.

    Parameters:
        invite_link (``str``):
            The invite link. If the link was created by another chat administrator, then the second part of the
            link will be replaced with "...".

        date (:py:obj:`~datetime.datetime`):
            The date when the link was created.

        is_primary (``bool``):
            True, if the link is primary.

        is_revoked (``bool``):
            True, if the link is revoked.

        creator (:obj:`~Octra.types.User`, *optional*):
            Creator of the link.

        name (``str``, *optional*):
            Invite link name

        creates_join_request (``bool``, *optional*):
            True, if users joining the chat via the link need to be approved by chat administrators.

        start_date (:py:obj:`~datetime.datetime`, *optional*):
            Point in time when the link has been edited.

        expire_date (:py:obj:`~datetime.datetime`, *optional*):
            Point in time when the link will expire or has been expired.

        USER_limit (``int``, *optional*):
            Maximum number of users that can be USERs of the chat simultaneously after joining the chat via this
            invite link; 1-99999.

        USER_count (``int``, *optional*):
            Number of users that joined via this link and are currently USER of the chat.

        pending_join_request_count (``int``, *optional*):
            Number of pending join requests created using this link
    """

    def __init__(
        self, *,
        invite_link: str,
        date: datetime,
        is_primary: bool = None,
        is_revoked: bool = None,
        creator: "types.User" = None,
        name: str = None,
        creates_join_request: bool = None,
        start_date: datetime = None,
        expire_date: datetime = None,
        USER_limit: int = None,
        USER_count: int = None,
        pending_join_request_count: int = None
    ):
        super().__init__()

        self.invite_link = invite_link
        self.date = date
        self.is_primary = is_primary
        self.is_revoked = is_revoked
        self.creator = creator
        self.name = name
        self.creates_join_request = creates_join_request
        self.start_date = start_date
        self.expire_date = expire_date
        self.USER_limit = USER_limit
        self.USER_count = USER_count
        self.pending_join_request_count = pending_join_request_count

    @staticmethod
    def _parse(
        client: "Octra.Client",
        invite: "raw.base.ExportedChatInvite",
        users: Dict[int, "raw.types.User"] = None
    ) -> Optional["ChatInviteLink"]:
        if not isinstance(invite, raw.types.ChatInviteExported):
            return None

        creator = (
            types.User._parse(client, users[invite.admin_id])
            if users is not None
            else None
        )

        return ChatInviteLink(
            invite_link=invite.link,
            date=utils.timestamp_to_datetime(invite.date),
            is_primary=invite.permanent,
            is_revoked=invite.revoked,
            creator=creator,
            name=invite.title,
            creates_join_request=invite.request_needed,
            start_date=utils.timestamp_to_datetime(invite.start_date),
            expire_date=utils.timestamp_to_datetime(invite.expire_date),
            USER_limit=invite.usage_limit,
            USER_count=invite.usage,
            pending_join_request_count=invite.requested
        )
