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


class RestrictChatUSER:
    async def restrict_chat_USER(
        self: "Octra.Client",
        chat_id: Union[int, str],
        octra_user_id: Union[int, str],
        permissions: "types.ChatPermissions",
        until_date: datetime = utils.zero_datetime()
    ) -> "types.Chat":
        """Restrict a user in a supergroup.

        You must be an administrator in the supergroup for this to work and must have the appropriate admin rights.
        Pass True for all permissions to lift restrictions from a user.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

            octra_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            permissions (:obj:`~Octra.types.ChatPermissions`):
                New user permissions.

            until_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the user will be unbanned.
                If user is banned for more than 366 days or less than 30 seconds from the current time they are
                considered to be banned forever. Defaults to epoch (ban forever).

        Returns:
            :obj:`~Octra.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                from datetime import datetime, timedelta
                from Octra.types import ChatPermissions

                # t.me/TheVenomXD Completely restrict chat USER (mute) forever
                await app.restrict_chat_USER(chat_id, octra_user_id, ChatPermissions())

                # t.me/TheVenomXD Chat USER muted for 24h
                await app.restrict_chat_USER(chat_id, octra_user_id, ChatPermissions(),
                    datetime.now() + timedelta(days=1))

                # t.me/TheVenomXD Chat USER can only send text messages
                await app.restrict_chat_USER(chat_id, octra_user_id,
                    ChatPermissions(can_send_messages=True))
        """
        r = await self.invoke(
            raw.functions.channels.EditBanned(
                channel=await self.resolve_peer(chat_id),
                participant=await self.resolve_peer(octra_user_id),
                banned_rights=raw.types.ChatBannedRights(
                    until_date=utils.datetime_to_timestamp(until_date),
                    send_messages=not permissions.can_send_messages,
                    send_media=not permissions.can_send_media_messages,
                    send_stickers=not permissions.can_send_other_messages,
                    send_gifs=not permissions.can_send_other_messages,
                    send_games=not permissions.can_send_other_messages,
                    send_inline=not permissions.can_send_other_messages,
                    embed_links=not permissions.can_add_web_page_previews,
                    send_polls=not permissions.can_send_polls,
                    change_info=not permissions.can_change_info,
                    invite_users=not permissions.can_invite_users,
                    pin_messages=not permissions.can_pin_messages,
                )
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])
