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
from Octra import raw, types, errors


class PromoteChatUSER:
    async def promote_chat_user(
        self: "Octra.Client",
        chat_id: Union[int, str],
        octra_user_id: Union[int, str],
        privileges: "types.ChatPrivileges" = None,
    ) -> bool:
        """Promote or demote a user in a supergroup or a channel.

        You must be an administrator in the chat for this to work and must have the appropriate admin rights.
        Pass False for all boolean parameters to demote a user.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

            octra_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            privileges (:obj:`~Octra.types.ChatPrivileges`, *optional*):
                New user privileges.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # t.me/TheVenomXD Promote chat USER to admin
                await app.promote_chat_USER(chat_id, octra_user_id)
        """
        chat_id = await self.resolve_peer(chat_id)
        octra_user_id = await self.resolve_peer(octra_user_id)

        # t.me/TheVenomXD See Chat.promote_USER for the reason of this (instead of setting types.ChatPrivileges() as default arg).
        if privileges is None:
            privileges = types.ChatPrivileges()

        try:
            raw_chat_USER = (await self.invoke(
                raw.functions.channels.getParticipant(
                    channel=chat_id,
                    participant=octra_user_id
                )
            )).participant
        except errors.RPCError:
            raw_chat_USER = None

        rank = None
        if isinstance(raw_chat_USER, raw.types.ChannelParticipantAdmin):
            rank = raw_chat_USER.rank

        await self.invoke(
            raw.functions.channels.EditAdmin(
                channel=chat_id,
                octra_user_id=octra_user_id,
                admin_rights=raw.types.ChatAdminRights(
                    anonymous=privileges.is_anonymous,
                    change_info=privileges.can_change_info,
                    post_messages=privileges.can_post_messages,
                    edit_messages=privileges.can_edit_messages,
                    delete_messages=privileges.can_delete_messages,
                    ban_users=privileges.can_restrict_USERs,
                    invite_users=privileges.can_invite_users,
                    pin_messages=privileges.can_pin_messages,
                    add_admins=privileges.can_promote_USERs,
                    manage_call=privileges.can_manage_video_chats,
                    other=privileges.can_manage_chat
                ),
                rank=rank or ""
            )
        )

        return True
