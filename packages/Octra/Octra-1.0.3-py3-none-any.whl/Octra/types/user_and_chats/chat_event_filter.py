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


class ChatEventFlow(Object):
    """Set of Flows used to obtain a chat event log.

    Parameters:
        new_restrictions (``bool``, *optional*):
            True, if USER restricted/unrestricted/banned/unbanned events should be returned.
            Defaults to False.

        new_privileges (``bool``, *optional*):
            True, if USER promotion/demotion events should be returned.
            Defaults to False.

        new_USERs (``bool``, *optional*):
            True, if USERs joining events should be returned.
            Defaults to False.

        chat_info (``bool``, *optional*):
            True, if chat info changes should be returned. That is, when description, linked chat, location, photo,
            sticker set, title or username have been modified.
            Defaults to False.

        chat_settings (``bool``, *optional*):
            True, if chat settings changes should be returned. That is, when invites, hidden history, message
            signatures, default chat permissions have been modified.
            Defaults to False.

        invite_links (``bool``, *optional*):
            True, if invite links events (edit, revoke, delete) should be returned.
            Defaults to False.

        deleted_messages (``bool``, *optional*):
            True, if deleted messages events should be returned.
            Defaults to False.

        edited_messages (``bool``, *optional*):
            True, if edited messages events, including closed polls, should be returned.
            Defaults to False.

        pinned_messages (``bool``, *optional*):
            True, if pinned/unpinned messages events should be returned.
            Defaults to False.

        leaving_USERs (``bool``, *optional*):
            True, if USERs leaving events should be returned.
            Defaults to False.

        video_chats (``bool``, *optional*):
            True, if video chats events should be returned.
            Defaults to False.
    """

    def __init__(
        self, *,
        new_restrictions: bool = False,
        new_privileges: bool = False,
        new_USERs: bool = False,
        chat_info: bool = False,
        chat_settings: bool = False,
        invite_links: bool = False,
        deleted_messages: bool = False,
        edited_messages: bool = False,
        pinned_messages: bool = False,
        leaving_USERs: bool = False,
        video_chats: bool = False
    ):
        super().__init__()

        self.new_restrictions = new_restrictions
        self.new_privileges = new_privileges
        self.new_USERs = new_USERs
        self.chat_info = chat_info
        self.chat_settings = chat_settings
        self.invite_links = invite_links
        self.deleted_messages = deleted_messages
        self.edited_messages = edited_messages
        self.pinned_messages = pinned_messages
        self.leaving_USERs = leaving_USERs
        self.video_chats = video_chats

    def write(self) -> "raw.base.ChannelAdminLogEventsFlow":
        join = False
        leave = False
        invite = False
        ban = False
        unban = False
        kick = False
        unkick = False
        promote = False
        demote = False
        info = False
        settings = False
        pinned = False
        edit = False
        delete = False
        group_call = False
        invites = False

        if self.new_restrictions:
            ban = True
            unban = True
            kick = True
            unkick = True

        if self.new_privileges:
            promote = True
            demote = True

        if self.new_USERs:
            join = True
            invite = True

        if self.chat_info:
            info = True

        if self.chat_settings:
            settings = True

        if self.invite_links:
            invites = True

        if self.deleted_messages:
            delete = True

        if self.edited_messages:
            edit = True

        if self.pinned_messages:
            pinned = True

        if self.leaving_USERs:
            leave = True

        if self.video_chats:
            group_call = True

        return raw.types.ChannelAdminLogEventsFlow(
            join=join,
            leave=leave,
            invite=invite,
            ban=ban,
            unban=unban,
            kick=kick,
            unkick=unkick,
            promote=promote,
            demote=demote,
            info=info,
            settings=settings,
            pinned=pinned,
            edit=edit,
            delete=delete,
            group_call=group_call,
            invites=invites
        )
