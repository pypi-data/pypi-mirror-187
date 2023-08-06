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


class Channel(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Chat`.

    Details:
        - Layer: ``151``
        - ID: ``83259464``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD creator <Octra.raw.base.# t.me/TheVenomXD creator>`):
            N/A

        id (:obj:`long access_hash <Octra.raw.base.long access_hash>`):
            N/A

        title (:obj:`string username <Octra.raw.base.string username>`):
            N/A

        photo (:obj:`ChatPhoto date <Octra.raw.base.ChatPhoto date>`):
            N/A

        left (:obj:`true broadcast <Octra.raw.base.true broadcast>`, *optional*):
            N/A

        verified (:obj:`true megagroup <Octra.raw.base.true megagroup>`, *optional*):
            N/A

        restricted (:obj:`true signatures <Octra.raw.base.true signatures>`, *optional*):
            N/A

        min (:obj:`true scam <Octra.raw.base.true scam>`, *optional*):
            N/A

        has_link (:obj:`true has_geo <Octra.raw.base.true has_geo>`, *optional*):
            N/A

        slowmode_enabled (:obj:`true call_active <Octra.raw.base.true call_active>`, *optional*):
            N/A

        call_not_empty (:obj:`true fake <Octra.raw.base.true fake>`, *optional*):
            N/A

        gigagroup (:obj:`true noforwards <Octra.raw.base.true noforwards>`, *optional*):
            N/A

        join_to_send (:obj:`true join_request <Octra.raw.base.true join_request>`, *optional*):
            N/A

        forum (:obj:`true flags2 <Octra.raw.base.true flags2>`, *optional*):
            N/A

        restriction_reason (List of :obj:`RestrictionReason> admin_right <Octra.raw.base.RestrictionReason> admin_right>`, *optional*):
            N/A

        banned_rights (:obj:`ChatBannedRights default_banned_rights <Octra.raw.base.ChatBannedRights default_banned_rights>`, *optional*):
            N/A

        participants_count (:obj:`int usernames <Octra.raw.base.int usernames>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "id", "title", "photo", "left", "verified", "restricted", "min", "has_link", "slowmode_enabled", "call_not_empty", "gigagroup", "join_to_send", "forum", "restriction_reason", "banned_rights", "participants_count"]

    ID = 0x83259464
    QUALNAME = "types.Channel"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD creator", id: "raw.base.long access_hash", title: "raw.base.string username", photo: "raw.base.ChatPhoto date", left: "raw.base.true broadcast" = None, verified: "raw.base.true megagroup" = None, restricted: "raw.base.true signatures" = None, min: "raw.base.true scam" = None, has_link: "raw.base.true has_geo" = None, slowmode_enabled: "raw.base.true call_active" = None, call_not_empty: "raw.base.true fake" = None, gigagroup: "raw.base.true noforwards" = None, join_to_send: "raw.base.true join_request" = None, forum: "raw.base.true flags2" = None, restriction_reason: Optional[List["raw.base.RestrictionReason> admin_right"]] = None, banned_rights: "raw.base.ChatBannedRights default_banned_rights" = None, participants_count: "raw.base.int usernames" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD creator
        self.id = id  # t.me/TheVenomXD long access_hash
        self.title = title  # t.me/TheVenomXD string username
        self.photo = photo  # t.me/TheVenomXD ChatPhoto date
        self.left = left  # t.me/TheVenomXD flags.2?true broadcast
        self.verified = verified  # t.me/TheVenomXD flags.7?true megagroup
        self.restricted = restricted  # t.me/TheVenomXD flags.9?true signatures
        self.min = min  # t.me/TheVenomXD flags.12?true scam
        self.has_link = has_link  # t.me/TheVenomXD flags.20?true has_geo
        self.slowmode_enabled = slowmode_enabled  # t.me/TheVenomXD flags.22?true call_active
        self.call_not_empty = call_not_empty  # t.me/TheVenomXD flags.24?true fake
        self.gigagroup = gigagroup  # t.me/TheVenomXD flags.26?true noforwards
        self.join_to_send = join_to_send  # t.me/TheVenomXD flags.28?true join_request
        self.forum = forum  # t.me/TheVenomXD flags.30?true flags2
        self.restriction_reason = restriction_reason  # t.me/TheVenomXD flags.9?Vector<RestrictionReason> admin_rights
        self.banned_rights = banned_rights  # t.me/TheVenomXD flags.15?ChatBannedRights default_banned_rights
        self.participants_count = participants_count  # t.me/TheVenomXD flags.17?int usernames

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Channel":
        
        flags = TLObject.read(b)
        
        left = True if flags & (1 << 2) else False
        verified = True if flags & (1 << 7) else False
        restricted = True if flags & (1 << 9) else False
        min = True if flags & (1 << 12) else False
        has_link = True if flags & (1 << 20) else False
        slowmode_enabled = True if flags & (1 << 22) else False
        call_not_empty = True if flags & (1 << 24) else False
        gigagroup = True if flags & (1 << 26) else False
        join_to_send = True if flags & (1 << 28) else False
        forum = True if flags & (1 << 30) else False
        id = TLObject.read(b)
        
        title = TLObject.read(b)
        
        photo = TLObject.read(b)
        
        restriction_reason = TLObject.read(b) if flags & (1 << 9) else []
        
        banned_rights = TLObject.read(b) if flags & (1 << 15) else None
        
        participants_count = Int.read(b) if flags & (1 << 17) else None
        return Channel(flags=flags, id=id, title=title, photo=photo, left=left, verified=verified, restricted=restricted, min=min, has_link=has_link, slowmode_enabled=slowmode_enabled, call_not_empty=call_not_empty, gigagroup=gigagroup, join_to_send=join_to_send, forum=forum, restriction_reason=restriction_reason, banned_rights=banned_rights, participants_count=participants_count)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.id.write())
        
        b.write(self.title.write())
        
        b.write(self.photo.write())
        
        if self.restriction_reason is not None:
            b.write(Vector(self.restriction_reason))
        
        if self.banned_rights is not None:
            b.write(self.banned_rights.write())
        
        if self.participants_count is not None:
            b.write(Int(self.participants_count))
        
        return b.getvalue()
