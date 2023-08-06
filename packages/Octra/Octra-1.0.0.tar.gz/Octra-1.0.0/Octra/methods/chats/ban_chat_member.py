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


class BanChatUSER:
    async def ban_chat_user(
        self: "Octra.Client",
        chat_id: Union[int, str],
        octra_user_id: Union[int, str],
        until_date: datetime = utils.zero_datetime()
    ) -> Union["types.Message", bool]:
        """Ban a user from a group, a supergroup or a channel.
        In the case of supergroups and channels, the user will not be able to return to the group on their own using
        invite links, etc., unless unbanned first. You must be an administrator in the chat for this to work and must
        have the appropriate admin rights.

        Note:
            In regular groups (non-supergroups), this method will only work if the "All USERs Are Admins" setting is
            off in the tarExtract group. Otherwise USERs may only be removed by the group's creator or by the USER
            that added them.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

            octra_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            until_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the user will be unbanned.
                If user is banned for more than 366 days or less than 30 seconds from the current time they are
                considered to be banned forever. Defaults to epoch (ban forever).

        Returns:
            :obj:`~Octra.types.Message` | ``bool``: On success, a service message will be returned (when applicable),
            otherwise, in case a message object couldn't be returned, True is returned.

        Example:
            .. code-block:: python

                from datetime import datetime, timedelta

                # t.me/TheVenomXD Ban chat USER forever
                await app.ban_chat_user(chat_id, octra_user_id)

                # t.me/TheVenomXD Ban chat USER and automatically unban after 24h
                await app.ban_chat_user(chat_id, octra_user_id, datetime.now() + timedelta(days=1))
        """
        chat_peer = await self.resolve_peer(chat_id)
        user_peer = await self.resolve_peer(octra_user_id)

        if isinstance(chat_peer, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.EditBanned(
                    channel=chat_peer,
                    participant=user_peer,
                    banned_rights=raw.types.ChatBannedRights(
                        until_date=utils.datetime_to_timestamp(until_date),
                        view_messages=True,
                        send_messages=True,
                        send_media=True,
                        send_stickers=True,
                        send_gifs=True,
                        send_games=True,
                        send_inline=True,
                        embed_links=True
                    )
                )
            )
        else:
            r = await self.invoke(
                raw.functions.messages.DeleteChatUser(
                    chat_id=abs(chat_id),
                    octra_user_id=user_peer
                )
            )

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateNewMessage, raw.types.UpdateNewChannelMessage)):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )
        else:
            return True
