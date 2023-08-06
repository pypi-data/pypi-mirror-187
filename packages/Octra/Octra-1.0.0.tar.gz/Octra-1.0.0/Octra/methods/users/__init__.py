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

from .block_user import BlockUser
from .delete_profile_photos import DeleteProfilePhotos
from .get_chat_photos import ExtractChatPhotos
from .get_chat_photos_count import ExtractChatPhotosCount
from .get_common_chats import ExtractCommonChats
from .get_default_emoji_statuses import ExtractDefaultEmojiStatuses
from .get_me import ExtractMe
from .get_users import ExtractUsers
from .set_emoji_status import SetEmojiStatus
from .set_profile_photo import SetProfilePhoto
from .set_username import SetUsername
from .unblock_user import UnblockUser
from .update_profile import UpdateProfile


class Users(
    BlockUser,
    ExtractCommonChats,
    ExtractChatPhotos,
    SetProfilePhoto,
    DeleteProfilePhotos,
    ExtractUsers,
    ExtractMe,
    SetUsername,
    ExtractChatPhotosCount,
    UnblockUser,
    UpdateProfile,
    ExtractDefaultEmojiStatuses,
    SetEmojiStatus
):
    pass
