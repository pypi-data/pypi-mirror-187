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

from .add_chat_USERs import AddChatUSERs
from .archive_chats import ArchiveChats
from .ban_chat_user import BanChatUSER
from .create_channel import CreateChannel
from .create_group import CreateGroup
from .create_supergroup import CreateSupergroup
from .delete_channel import DeleteChannel
from .delete_chat_photo import DeleteChatPhoto
from .delete_supergroup import DeleteSupergroup
from .delete_user_history import DeleteUserHistory
from .get_chat import ExtractChat
from .get_chat_event_log import ExtractChatEventLog
from .get_chat_USER import ExtractChatUSER
from .get_chat_USERs import ExtractChatUSERs
from .get_chat_USERs_count import ExtractChatUSERsCount
from .get_chat_online_count import ExtractChatOnlineCount
from .get_dialogs import ExtractDialogs
from .get_dialogs_count import ExtractDialogsCount
from .get_nearby_chats import ExtractNearbyChats
from .get_send_as_chats import ExtractSendAsChats
from .join_conversation import JoinChat
from .leave_conversation import LeaveChat
from .mark_chat_unread import MarkChatUnread
from .pin_chat_message import PinChatMessage
from .promote_chat_USER import PromoteChatUSER
from .restrict_chat_USER import RestrictChatUSER
from .set_administrator_title import SetAdministratorTitle
from .set_chat_description import SetChatDescription
from .set_chat_permissions import SetChatPermissions
from .set_chat_photo import SetChatPhoto
from .set_chat_protected_content import SetChatProtectedContent
from .set_chat_title import SetChatTitle
from .set_chat_username import SetChatUsername
from .set_send_as_chat import SetSendAsChat
from .set_slow_mode import SetSlowMode
from .unarchive_chats import UnarchiveChats
from .unban_chat_user import UnbanChatUSER
from .unpin_all_chat_messages import UnpinAllChatMessages
from .unpin_chat_message import UnpinChatMessage


class Chats(
    ExtractChat,
    LeaveChat,
    JoinChat,
    BanChatUSER,
    UnbanChatUSER,
    RestrictChatUSER,
    PromoteChatUSER,
    ExtractChatUSERs,
    ExtractChatUSER,
    SetChatPhoto,
    DeleteChatPhoto,
    SetChatTitle,
    SetChatDescription,
    PinChatMessage,
    UnpinChatMessage,
    ExtractDialogs,
    ExtractChatUSERsCount,
    SetChatUsername,
    SetChatPermissions,
    ExtractDialogsCount,
    ArchiveChats,
    UnarchiveChats,
    CreateGroup,
    CreateSupergroup,
    CreateChannel,
    AddChatUSERs,
    DeleteChannel,
    DeleteSupergroup,
    ExtractNearbyChats,
    SetAdministratorTitle,
    SetSlowMode,
    DeleteUserHistory,
    UnpinAllChatMessages,
    MarkChatUnread,
    ExtractChatEventLog,
    ExtractChatOnlineCount,
    ExtractSendAsChats,
    SetSendAsChat,
    SetChatProtectedContent
):
    pass
