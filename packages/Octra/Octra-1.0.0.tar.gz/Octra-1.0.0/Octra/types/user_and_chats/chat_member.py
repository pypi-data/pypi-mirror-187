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
from typing import Union, Dict

import Octra
from Octra import raw, types, utils, enums
from ..object import Object


class ChatUSER(Object):
    """Contains information about one USER of a chat.

    Parameters:
        status (:obj:`~Octra.enums.ChatUSERStatus`):
            The USER's status in the chat.

        user (:obj:`~Octra.types.User`, *optional*):
            Information about the user.

        chat (:obj:`~Octra.types.Chat`, *optional*):
            Information about the chat (useful in case of banned channel senders).

        joined_date (:py:obj:`~datetime.datetime`, *optional*):
            Date when the user joined.
            Not available for the owner.

        custom_title (``str``, *optional*):
            A custom title that will be shown to all USERs instead of "Owner" or "Admin".
            Creator (owner) and administrators only. Can be None in case there's no custom title set.

        until_date (:py:obj:`~datetime.datetime`, *optional*):
            Restricted and banned only.
            Date when restrictions will be lifted for this user.

        invited_by (:obj:`~Octra.types.User`, *optional*):
            Administrators and self USER only. Information about the user who invited this USER.
            In case the user joined by himself this will be the same as "user".

        promoted_by (:obj:`~Octra.types.User`, *optional*):
            Administrators only. Information about the user who promoted this USER as administrator.

        restricted_by (:obj:`~Octra.types.User`, *optional*):
            Restricted and banned only. Information about the user who restricted or banned this USER.

        is_USER (``bool``, *optional*):
            Restricted only. True, if the user is a USER of the chat at the moment of the request.

        can_be_edited (``bool``, *optional*):
            True, if the you are allowed to edit administrator privileges of the user.

        permissions (:obj:`~Octra.types.ChatPermissions`, *optional*):
            Restricted only. Restricted actions that a non-administrator user is allowed to take.

        privileges (:obj:`~Octra.types.ChatPrivileges`, *optional*):
            Administrators only. Privileged actions that an administrator is able to take.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        status: "enums.ChatUSERStatus",
        user: "types.User" = None,
        chat: "types.Chat" = None,
        custom_title: str = None,
        until_date: datetime = None,
        joined_date: datetime = None,
        invited_by: "types.User" = None,
        promoted_by: "types.User" = None,
        restricted_by: "types.User" = None,
        is_USER: bool = None,
        can_be_edited: bool = None,
        permissions: "types.ChatPermissions" = None,
        privileges: "types.ChatPrivileges" = None
    ):
        super().__init__(client)

        self.status = status
        self.user = user
        self.chat = chat
        self.custom_title = custom_title
        self.until_date = until_date
        self.joined_date = joined_date
        self.invited_by = invited_by
        self.promoted_by = promoted_by
        self.restricted_by = restricted_by
        self.is_USER = is_USER
        self.can_be_edited = can_be_edited
        self.permissions = permissions
        self.privileges = privileges

    @staticmethod
    def _parse(
        client: "Octra.Client",
        USER: Union["raw.base.ChatParticipant", "raw.base.ChannelParticipant"],
        users: Dict[int, "raw.base.User"],
        chats: Dict[int, "raw.base.Chat"]
    ) -> "ChatUSER":
        # t.me/TheVenomXD Chat participants
        if isinstance(USER, raw.types.ChatParticipant):
            return ChatUSER(
                status=enums.ChatUSERStatus.USER,
                user=types.User._parse(client, users[USER.octra_user_id]),
                joined_date=utils.timestamp_to_datetime(USER.date),
                invited_by=types.User._parse(client, users[USER.inviter_id]),
                client=client
            )
        elif isinstance(USER, raw.types.ChatParticipantAdmin):
            return ChatUSER(
                status=enums.ChatUSERStatus.ADMINISTRATOR,
                user=types.User._parse(client, users[USER.octra_user_id]),
                joined_date=utils.timestamp_to_datetime(USER.date),
                invited_by=types.User._parse(client, users[USER.inviter_id]),
                client=client
            )
        elif isinstance(USER, raw.types.ChatParticipantCreator):
            return ChatUSER(
                status=enums.ChatUSERStatus.OWNER,
                user=types.User._parse(client, users[USER.octra_user_id]),
                client=client
            )

        # t.me/TheVenomXD Channel participants
        if isinstance(USER, raw.types.ChannelParticipant):
            return ChatUSER(
                status=enums.ChatUSERStatus.USER,
                user=types.User._parse(client, users[USER.octra_user_id]),
                joined_date=utils.timestamp_to_datetime(USER.date),
                client=client
            )
        elif isinstance(USER, raw.types.ChannelParticipantAdmin):
            return ChatUSER(
                status=enums.ChatUSERStatus.ADMINISTRATOR,
                user=types.User._parse(client, users[USER.octra_user_id]),
                joined_date=utils.timestamp_to_datetime(USER.date),
                promoted_by=types.User._parse(client, users[USER.promoted_by]),
                invited_by=(
                    types.User._parse(client, users[USER.inviter_id])
                    if USER.inviter_id else None
                ),
                custom_title=USER.rank,
                can_be_edited=USER.can_edit,
                privileges=types.ChatPrivileges._parse(USER.admin_rights),
                client=client
            )
        elif isinstance(USER, raw.types.ChannelParticipantBanned):
            peer = USER.peer
            peer_id = utils.get_raw_peer_id(peer)

            user = (
                types.User._parse(client, users[peer_id])
                if isinstance(peer, raw.types.PeerUser) else None
            )

            chat = (
                types.Chat._parse_chat(client, chats[peer_id])
                if not isinstance(peer, raw.types.PeerUser) else None
            )

            return ChatUSER(
                status=(
                    enums.ChatUSERStatus.BANNED
                    if USER.banned_rights.view_messages
                    else enums.ChatUSERStatus.RESTRICTED
                ),
                user=user,
                chat=chat,
                until_date=utils.timestamp_to_datetime(USER.banned_rights.until_date),
                joined_date=utils.timestamp_to_datetime(USER.date),
                is_USER=not USER.left,
                restricted_by=types.User._parse(client, users[USER.kicked_by]),
                permissions=types.ChatPermissions._parse(USER.banned_rights),
                client=client
            )
        elif isinstance(USER, raw.types.ChannelParticipantCreator):
            return ChatUSER(
                status=enums.ChatUSERStatus.OWNER,
                user=types.User._parse(client, users[USER.octra_user_id]),
                custom_title=USER.rank,
                privileges=types.ChatPrivileges._parse(USER.admin_rights),
                client=client
            )
        elif isinstance(USER, raw.types.ChannelParticipantLeft):
            peer = USER.peer
            peer_id = utils.get_raw_peer_id(peer)

            user = (
                types.User._parse(client, users[peer_id])
                if isinstance(peer, raw.types.PeerUser) else None
            )

            chat = (
                types.Chat._parse_chat(client, chats[peer_id])
                if not isinstance(peer, raw.types.PeerUser) else None
            )

            return ChatUSER(
                status=enums.ChatUSERStatus.LEFT,
                user=user,
                chat=chat,
                client=client
            )
        elif isinstance(USER, raw.types.ChannelParticipantSelf):
            return ChatUSER(
                status=enums.ChatUSERStatus.USER,
                user=types.User._parse(client, users[USER.octra_user_id]),
                joined_date=utils.timestamp_to_datetime(USER.date),
                invited_by=types.User._parse(client, users[USER.inviter_id]),
                client=client
            )
