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

from io import BytesIO

from Octra.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from Octra.raw.core import TLObject
from Octra import raw
from typing import List, Optional, Any

# t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD
# t.me/TheVenomXD               !!! WARNING !!!               # t.me/TheVenomXD
# t.me/TheVenomXD          This is a generated file!          # t.me/TheVenomXD
# t.me/TheVenomXD All changes made in this file will be lost! # t.me/TheVenomXD
# t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD


class UserFull(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.UserFull`.

    Details:
        - Layer: ``151``
        - ID: ``F8D32AED``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD blocked <Octra.raw.base.# t.me/TheVenomXD blocked>`):
            N/A

        id (:obj:`long about <Octra.raw.base.long about>`):
            N/A

        settings (:obj:`PeerSettings personal_photo <Octra.raw.base.PeerSettings personal_photo>`):
            N/A

        notify_settings (:obj:`PeerNotifySettings bot_info <Octra.raw.base.PeerNotifySettings bot_info>`):
            N/A

        phone_calls_available (:obj:`true phone_calls_private <Octra.raw.base.true phone_calls_private>`, *optional*):
            N/A

        can_pin_message (:obj:`true has_scheduled <Octra.raw.base.true has_scheduled>`, *optional*):
            N/A

        video_calls_available (:obj:`true voice_messages_forbidden <Octra.raw.base.true voice_messages_forbidden>`, *optional*):
            N/A

        profile_photo (:obj:`Photo fallback_photo <Octra.raw.base.Photo fallback_photo>`, *optional*):
            N/A

        pinned_msg_id (:obj:`int common_chats_count <Octra.raw.base.int common_chats_count>`, *optional*):
            N/A

        folder_id (:obj:`int ttl_period <Octra.raw.base.int ttl_period>`, *optional*):
            N/A

        theme_emoticon (:obj:`string private_forward_name <Octra.raw.base.string private_forward_name>`, *optional*):
            N/A

        bot_group_admin_rights (:obj:`ChatAdminRights bot_broadcast_admin_rights <Octra.raw.base.ChatAdminRights bot_broadcast_admin_rights>`, *optional*):
            N/A

        premium_gifts (List of :obj:`PremiumGiftOption> <Octra.raw.base.PremiumGiftOption>>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "id", "settings", "notify_settings", "phone_calls_available", "can_pin_message", "video_calls_available", "profile_photo", "pinned_msg_id", "folder_id", "theme_emoticon", "bot_group_admin_rights", "premium_gifts"]

    ID = 0xf8d32aed
    QUALNAME = "types.UserFull"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD blocked", id: "raw.base.long about", settings: "raw.base.PeerSettings personal_photo", notify_settings: "raw.base.PeerNotifySettings bot_info", phone_calls_available: "raw.base.true phone_calls_private" = None, can_pin_message: "raw.base.true has_scheduled" = None, video_calls_available: "raw.base.true voice_messages_forbidden" = None, profile_photo: "raw.base.Photo fallback_photo" = None, pinned_msg_id: "raw.base.int common_chats_count" = None, folder_id: "raw.base.int ttl_period" = None, theme_emoticon: "raw.base.string private_forward_name" = None, bot_group_admin_rights: "raw.base.ChatAdminRights bot_broadcast_admin_rights" = None, premium_gifts: Optional[List["raw.base.PremiumGiftOption>"]] = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD blocked
        self.id = id  # t.me/TheVenomXD long about
        self.settings = settings  # t.me/TheVenomXD PeerSettings personal_photo
        self.notify_settings = notify_settings  # t.me/TheVenomXD PeerNotifySettings bot_info
        self.phone_calls_available = phone_calls_available  # t.me/TheVenomXD flags.4?true phone_calls_private
        self.can_pin_message = can_pin_message  # t.me/TheVenomXD flags.7?true has_scheduled
        self.video_calls_available = video_calls_available  # t.me/TheVenomXD flags.13?true voice_messages_forbidden
        self.profile_photo = profile_photo  # t.me/TheVenomXD flags.2?Photo fallback_photo
        self.pinned_msg_id = pinned_msg_id  # t.me/TheVenomXD flags.6?int common_chats_count
        self.folder_id = folder_id  # t.me/TheVenomXD flags.11?int ttl_period
        self.theme_emoticon = theme_emoticon  # t.me/TheVenomXD flags.15?string private_forward_name
        self.bot_group_admin_rights = bot_group_admin_rights  # t.me/TheVenomXD flags.17?ChatAdminRights bot_broadcast_admin_rights
        self.premium_gifts = premium_gifts  # t.me/TheVenomXD flags.19?Vector<PremiumGiftOption> 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UserFull":
        
        flags = TLObject.read(b)
        
        phone_calls_available = True if flags & (1 << 4) else False
        can_pin_message = True if flags & (1 << 7) else False
        video_calls_available = True if flags & (1 << 13) else False
        id = TLObject.read(b)
        
        settings = TLObject.read(b)
        
        profile_photo = TLObject.read(b) if flags & (1 << 2) else None
        
        notify_settings = TLObject.read(b)
        
        pinned_msg_id = Int.read(b) if flags & (1 << 6) else None
        folder_id = Int.read(b) if flags & (1 << 11) else None
        theme_emoticon = String.read(b) if flags & (1 << 15) else None
        bot_group_admin_rights = TLObject.read(b) if flags & (1 << 17) else None
        
        premium_gifts = TLObject.read(b) if flags & (1 << 19) else []
        
        return UserFull(flags=flags, id=id, settings=settings, notify_settings=notify_settings, phone_calls_available=phone_calls_available, can_pin_message=can_pin_message, video_calls_available=video_calls_available, profile_photo=profile_photo, pinned_msg_id=pinned_msg_id, folder_id=folder_id, theme_emoticon=theme_emoticon, bot_group_admin_rights=bot_group_admin_rights, premium_gifts=premium_gifts)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.id.write())
        
        b.write(self.settings.write())
        
        if self.profile_photo is not None:
            b.write(self.profile_photo.write())
        
        b.write(self.notify_settings.write())
        
        if self.pinned_msg_id is not None:
            b.write(Int(self.pinned_msg_id))
        
        if self.folder_id is not None:
            b.write(Int(self.folder_id))
        
        if self.theme_emoticon is not None:
            b.write(String(self.theme_emoticon))
        
        if self.bot_group_admin_rights is not None:
            b.write(self.bot_group_admin_rights.write())
        
        if self.premium_gifts is not None:
            b.write(Vector(self.premium_gifts))
        
        return b.getvalue()
