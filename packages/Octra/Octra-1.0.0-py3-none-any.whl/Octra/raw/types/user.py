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


class User(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.User`.

    Details:
        - Layer: ``151``
        - ID: ``8F97C628``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD self <Octra.raw.base.# t.me/TheVenomXD self>`):
            N/A

        id (:obj:`long access_hash <Octra.raw.base.long access_hash>`):
            N/A

        contact (:obj:`true mutual_contact <Octra.raw.base.true mutual_contact>`, *optional*):
            N/A

        deleted (:obj:`true bot <Octra.raw.base.true bot>`, *optional*):
            N/A

        bot_chat_history (:obj:`true bot_nochats <Octra.raw.base.true bot_nochats>`, *optional*):
            N/A

        verified (:obj:`true restricted <Octra.raw.base.true restricted>`, *optional*):
            N/A

        min (:obj:`true bot_inline_geo <Octra.raw.base.true bot_inline_geo>`, *optional*):
            N/A

        support (:obj:`true scam <Octra.raw.base.true scam>`, *optional*):
            N/A

        apply_min_photo (:obj:`true fake <Octra.raw.base.true fake>`, *optional*):
            N/A

        bot_attach_menu (:obj:`true premium <Octra.raw.base.true premium>`, *optional*):
            N/A

        attach_menu_enabled (:obj:`true flags2 <Octra.raw.base.true flags2>`, *optional*):
            N/A

        first_name (:obj:`string last_name <Octra.raw.base.string last_name>`, *optional*):
            N/A

        username (:obj:`string phone <Octra.raw.base.string phone>`, *optional*):
            N/A

        photo (:obj:`UserProfilePhoto status <Octra.raw.base.UserProfilePhoto status>`, *optional*):
            N/A

        bot_info_version (:obj:`int restriction_reason <Octra.raw.base.int restriction_reason>`, *optional*):
            N/A

        bot_inline_placeholder (:obj:`string lang_code <Octra.raw.base.string lang_code>`, *optional*):
            N/A

        emoji_status (:obj:`EmojiStatus usernames <Octra.raw.base.EmojiStatus usernames>`, *optional*):
            N/A

    Functions:
        This object can be returned by 5 functions.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            account.UpdateProfile
            account.UpdateUsername
            account.ChangePhone
            users.GetUsers
            contacts.ImportContactToken
    """

    __slots__: List[str] = ["flags", "id", "contact", "deleted", "bot_chat_history", "verified", "min", "support", "apply_min_photo", "bot_attach_menu", "attach_menu_enabled", "first_name", "username", "photo", "bot_info_version", "bot_inline_placeholder", "emoji_status"]

    ID = 0x8f97c628
    QUALNAME = "types.User"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD self", id: "raw.base.long access_hash", contact: "raw.base.true mutual_contact" = None, deleted: "raw.base.true bot" = None, bot_chat_history: "raw.base.true bot_nochats" = None, verified: "raw.base.true restricted" = None, min: "raw.base.true bot_inline_geo" = None, support: "raw.base.true scam" = None, apply_min_photo: "raw.base.true fake" = None, bot_attach_menu: "raw.base.true premium" = None, attach_menu_enabled: "raw.base.true flags2" = None, first_name: "raw.base.string last_name" = None, username: "raw.base.string phone" = None, photo: "raw.base.UserProfilePhoto status" = None, bot_info_version: "raw.base.int restriction_reason" = None, bot_inline_placeholder: "raw.base.string lang_code" = None, emoji_status: "raw.base.EmojiStatus usernames" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD self
        self.id = id  # t.me/TheVenomXD long access_hash
        self.contact = contact  # t.me/TheVenomXD flags.11?true mutual_contact
        self.deleted = deleted  # t.me/TheVenomXD flags.13?true bot
        self.bot_chat_history = bot_chat_history  # t.me/TheVenomXD flags.15?true bot_nochats
        self.verified = verified  # t.me/TheVenomXD flags.17?true restricted
        self.min = min  # t.me/TheVenomXD flags.20?true bot_inline_geo
        self.support = support  # t.me/TheVenomXD flags.23?true scam
        self.apply_min_photo = apply_min_photo  # t.me/TheVenomXD flags.25?true fake
        self.bot_attach_menu = bot_attach_menu  # t.me/TheVenomXD flags.27?true premium
        self.attach_menu_enabled = attach_menu_enabled  # t.me/TheVenomXD flags.29?true flags2
        self.first_name = first_name  # t.me/TheVenomXD flags.1?string last_name
        self.username = username  # t.me/TheVenomXD flags.3?string phone
        self.photo = photo  # t.me/TheVenomXD flags.5?UserProfilePhoto status
        self.bot_info_version = bot_info_version  # t.me/TheVenomXD flags.14?int restriction_reason
        self.bot_inline_placeholder = bot_inline_placeholder  # t.me/TheVenomXD flags.19?string lang_code
        self.emoji_status = emoji_status  # t.me/TheVenomXD flags.30?EmojiStatus usernames

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "User":
        
        flags = TLObject.read(b)
        
        contact = True if flags & (1 << 11) else False
        deleted = True if flags & (1 << 13) else False
        bot_chat_history = True if flags & (1 << 15) else False
        verified = True if flags & (1 << 17) else False
        min = True if flags & (1 << 20) else False
        support = True if flags & (1 << 23) else False
        apply_min_photo = True if flags & (1 << 25) else False
        bot_attach_menu = True if flags & (1 << 27) else False
        attach_menu_enabled = True if flags & (1 << 29) else False
        id = TLObject.read(b)
        
        first_name = String.read(b) if flags & (1 << 1) else None
        username = String.read(b) if flags & (1 << 3) else None
        photo = TLObject.read(b) if flags & (1 << 5) else None
        
        bot_info_version = Int.read(b) if flags & (1 << 14) else None
        bot_inline_placeholder = String.read(b) if flags & (1 << 19) else None
        emoji_status = TLObject.read(b) if flags & (1 << 30) else None
        
        return User(flags=flags, id=id, contact=contact, deleted=deleted, bot_chat_history=bot_chat_history, verified=verified, min=min, support=support, apply_min_photo=apply_min_photo, bot_attach_menu=bot_attach_menu, attach_menu_enabled=attach_menu_enabled, first_name=first_name, username=username, photo=photo, bot_info_version=bot_info_version, bot_inline_placeholder=bot_inline_placeholder, emoji_status=emoji_status)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.id.write())
        
        if self.first_name is not None:
            b.write(String(self.first_name))
        
        if self.username is not None:
            b.write(String(self.username))
        
        if self.photo is not None:
            b.write(self.photo.write())
        
        if self.bot_info_version is not None:
            b.write(Int(self.bot_info_version))
        
        if self.bot_inline_placeholder is not None:
            b.write(String(self.bot_inline_placeholder))
        
        if self.emoji_status is not None:
            b.write(self.emoji_status.write())
        
        return b.getvalue()
