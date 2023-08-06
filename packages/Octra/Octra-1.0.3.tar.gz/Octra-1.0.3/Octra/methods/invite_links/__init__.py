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


from .approve_all_chat_join_requests import ApproveAllChatJoinRequests
from .approve_chat_join_request import ApproveChatJoinRequest
from .create_chat_invite_link import CreateChatInviteLink
from .decline_all_chat_join_requests import DeclineAllChatJoinRequests
from .decline_chat_join_request import DeclineChatJoinRequest
from .delete_chat_admin_invite_links import DeleteChatAdminInviteLinks
from .delete_chat_invite_link import DeleteChatInviteLink
from .edit_chat_invite_link import EditChatInviteLink
from .export_chat_invite_link import ExportChatInviteLink
from .get_chat_admin_invite_links import ExtractChatAdminInviteLinks
from .get_chat_admin_invite_links_count import ExtractChatAdminInviteLinksCount
from .get_chat_admins_with_invite_links import ExtractChatAdminsWithInviteLinks
from .get_chat_invite_link import ExtractChatInviteLink
from .get_chat_invite_link_joiners import ExtractChatInviteLinkJoiners
from .get_chat_invite_link_joiners_count import ExtractChatInviteLinkJoinersCount
from .get_chat_join_requests import ExtractChatJoinRequests
from .revoke_chat_invite_link import RevokeChatInviteLink


class InviteLinks(
    RevokeChatInviteLink,
    DeleteChatInviteLink,
    EditChatInviteLink,
    CreateChatInviteLink,
    ExtractChatInviteLinkJoiners,
    ExtractChatInviteLinkJoinersCount,
    ExtractChatAdminInviteLinks,
    ExportChatInviteLink,
    DeleteChatAdminInviteLinks,
    ExtractChatAdminInviteLinksCount,
    ExtractChatAdminsWithInviteLinks,
    ExtractChatInviteLink,
    ApproveChatJoinRequest,
    DeclineChatJoinRequest,
    ApproveAllChatJoinRequests,
    DeclineAllChatJoinRequests,
    ExtractChatJoinRequests
):
    pass
