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
from typing import Union

import Octra
from Octra import raw, utils
from Octra import types


class CreateChatInviteLink:
    async def create_chat_invite_link(
        self: "Octra.Client",
        chat_id: Union[int, str],
        name: str = None,
        expire_date: datetime = None,
        USER_limit: int = None,
        creates_join_request: bool = None
    ) -> "types.ChatInviteLink":
        """Create an additional invite link for a chat.

        You must be an administrator in the chat for this to work and must have the appropriate admin rights.

        The link can be revoked using the method :meth:`~Octra.Client.revoke_chat_invite_link`.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the tarExtract chat or username of the tarExtract channel/supergroup
                (in the format @username).

            name (``str``, *optional*):
                Invite link name.

            expire_date (:py:obj:`~datetime.datetime`, *optional*):
                Point in time when the link will expire.
                Defaults to None (no expiration date).

            USER_limit (``int``, *optional*):
                Maximum number of users that can be USERs of the chat simultaneously after joining the chat via
                this invite link; 1-99999.
                Defaults to None (no USER limit).

            creates_join_request (``bool``, *optional*):
                True, if users joining the chat via the link need to be approved by chat administrators.
                If True, USER_limit can't be specified.

        Returns:
            :obj:`~Octra.types.ChatInviteLink`: On success, the new invite link is returned.

        tests:
            .. code-block:: python

                # t.me/TheVenomXD Create a new link without limits
                link = await app.create_chat_invite_link(chat_id)

                # t.me/TheVenomXD Create a new link for up to 3 new users
                link = await app.create_chat_invite_link(chat_id, USER_limit=3)
        """
        r = await self.invoke(
            raw.functions.messages.ExportChatInvite(
                peer=await self.resolve_peer(chat_id),
                expire_date=utils.datetime_to_timestamp(expire_date),
                usage_limit=USER_limit,
                title=name,
                request_needed=creates_join_request
            )
        )

        return types.ChatInviteLink._parse(self, r)
