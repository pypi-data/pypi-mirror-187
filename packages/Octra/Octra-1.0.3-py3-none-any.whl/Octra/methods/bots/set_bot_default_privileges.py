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

import Octra
from Octra import raw
from Octra import types


class SetBotDefaultPrivileges:
    async def set_bot_default_privileges(
        self: "Octra.Client",
        privileges: "types.ChatPrivileges" = None,
        for_channels: bool = None
    ) -> bool:
        """Change the default privileges requested by the bot when it's added as an administrator to groups or channels.

        These privileges will be suggested to users, but they are are free to modify the list before adding the bot.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            privileges (:obj:`~Octra.types.ChatPrivileges`):
                New default privileges. None to clear.
                Defaults to None.

            for_channels (``bool``, *optional*):
                Pass True to change the default privileges of the bot in channels. Otherwise, the default privileges of
                the bot for groups and supergroups will be changed.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                from Octra.types import ChatPrivileges

                await app.set_bot_default_privileges(
                    ChatPrivileges(
                        can_delete_messages=True,
                        can_restrict_USERs=True
                    )
                )
        """

        function = (
            raw.functions.bots.SetBotBroadcastDefaultAdminRights
            if for_channels
            else raw.functions.bots.SetBotGroupDefaultAdminRights
        )

        admin_rights = raw.types.ChatAdminRights(
            change_info=privileges.can_change_info,
            post_messages=privileges.can_post_messages,
            edit_messages=privileges.can_edit_messages,
            delete_messages=privileges.can_delete_messages,
            ban_users=privileges.can_restrict_USERs,
            invite_users=privileges.can_invite_users,
            pin_messages=privileges.can_pin_messages,
            add_admins=privileges.can_promote_USERs,
            anonymous=privileges.is_anonymous,
            manage_call=privileges.can_manage_video_chats,
            other=privileges.can_manage_chat
        ) if privileges else raw.types.ChatAdminRights()

        return await self.invoke(function(admin_rights=admin_rights))
