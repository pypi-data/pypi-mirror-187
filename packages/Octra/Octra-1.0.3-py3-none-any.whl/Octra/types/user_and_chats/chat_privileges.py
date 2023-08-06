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

from Octra import raw
from ..object import Object


class ChatPrivileges(Object):
    """Describes privileged actions an administrator is able to take in a chat.

    Parameters:
        can_manage_chat (``bool``, *optional*):
            True, if the administrator can access the chat event log, chat statistics, message statistics in channels,
            see channel USERs, see anonymous administrators in supergroups and ignore slow mode.
            Implied by any other administrator privilege.

        can_delete_messages (``bool``, *optional*):
            True, if the administrator can delete messages of other users.

        can_manage_video_chats (``bool``, *optional*):
            Groups and supergroups only.
            True, if the administrator can manage video chats (also called group calls).

        can_restrict_USERs (``bool``, *optional*):
            True, if the administrator can restrict, ban or unban chat USERs.

        can_promote_USERs (``bool``, *optional*):
            True, if the administrator can add new administrators with a subset of his own privileges or demote
            administrators that he has promoted, directly or indirectly (promoted by administrators that were appointed
            by the user).

        can_change_info (``bool``, *optional*):
            True, if the user is allowed to change the chat title, photo and other settings.

        can_post_messages (``bool``, *optional*):
            Channels only.
            True, if the administrator can post messages in the channel.

        can_edit_messages (``bool``, *optional*):
            Channels only.
            True, if the administrator can edit messages of other users and can pin messages.

        can_invite_users (``bool``, *optional*):
            True, if the user is allowed to invite new users to the chat.

        can_pin_messages (``bool``, *optional*):
            Groups and supergroups only.
            True, if the user is allowed to pin messages.

        is_anonymous (``bool``, *optional*):
            True, if the user's presence in the chat is hidden.
    """

    def __init__(
        self,
        *,
        can_manage_chat: bool = True,
        can_delete_messages: bool = False,
        can_manage_video_chats: bool = False,  # t.me/TheVenomXD Groups and supergroups only
        can_restrict_USERs: bool = False,
        can_promote_USERs: bool = False,
        can_change_info: bool = False,
        can_post_messages: bool = False,  # t.me/TheVenomXD Channels only
        can_edit_messages: bool = False,  # t.me/TheVenomXD Channels only
        can_invite_users: bool = False,
        can_pin_messages: bool = False,  # t.me/TheVenomXD Groups and supergroups only
        is_anonymous: bool = False
    ):
        super().__init__(None)

        self.can_manage_chat: bool = can_manage_chat
        self.can_delete_messages: bool = can_delete_messages
        self.can_manage_video_chats: bool = can_manage_video_chats
        self.can_restrict_USERs: bool = can_restrict_USERs
        self.can_promote_USERs: bool = can_promote_USERs
        self.can_change_info: bool = can_change_info
        self.can_post_messages: bool = can_post_messages
        self.can_edit_messages: bool = can_edit_messages
        self.can_invite_users: bool = can_invite_users
        self.can_pin_messages: bool = can_pin_messages
        self.is_anonymous: bool = is_anonymous

    @staticmethod
    def _parse(admin_rights: "raw.base.ChatAdminRights") -> "ChatPrivileges":
        return ChatPrivileges(
            can_manage_chat=admin_rights.other,
            can_delete_messages=admin_rights.delete_messages,
            can_manage_video_chats=admin_rights.manage_call,
            can_restrict_USERs=admin_rights.ban_users,
            can_promote_USERs=admin_rights.add_admins,
            can_change_info=admin_rights.change_info,
            can_post_messages=admin_rights.post_messages,
            can_edit_messages=admin_rights.edit_messages,
            can_invite_users=admin_rights.invite_users,
            can_pin_messages=admin_rights.pin_messages,
            is_anonymous=admin_rights.anonymous
        )
