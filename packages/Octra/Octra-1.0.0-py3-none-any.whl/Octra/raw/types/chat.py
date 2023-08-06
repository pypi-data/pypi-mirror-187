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


class Chat(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Chat`.

    Details:
        - Layer: ``151``
        - ID: ``41CBF256``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD creator <Octra.raw.base.# t.me/TheVenomXD creator>`):
            N/A

        title (:obj:`string photo <Octra.raw.base.string photo>`):
            N/A

        participants_count (:obj:`int date <Octra.raw.base.int date>`):
            N/A

        version (:obj:`int migrated_to <Octra.raw.base.int migrated_to>`):
            N/A

        left (:obj:`true deactivated <Octra.raw.base.true deactivated>`, *optional*):
            N/A

        call_active (:obj:`true call_not_empty <Octra.raw.base.true call_not_empty>`, *optional*):
            N/A

        noforwards (:obj:`true id <Octra.raw.base.true id>`, *optional*):
            N/A

        admin_rights (:obj:`ChatAdminRights default_banned_rights <Octra.raw.base.ChatAdminRights default_banned_rights>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "title", "participants_count", "version", "left", "call_active", "noforwards", "admin_rights"]

    ID = 0x41cbf256
    QUALNAME = "types.Chat"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD creator", title: "raw.base.string photo", participants_count: "raw.base.int date", version: "raw.base.int migrated_to", left: "raw.base.true deactivated" = None, call_active: "raw.base.true call_not_empty" = None, noforwards: "raw.base.true id" = None, admin_rights: "raw.base.ChatAdminRights default_banned_rights" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD creator
        self.title = title  # t.me/TheVenomXD string photo
        self.participants_count = participants_count  # t.me/TheVenomXD int date
        self.version = version  # t.me/TheVenomXD int migrated_to
        self.left = left  # t.me/TheVenomXD flags.2?true deactivated
        self.call_active = call_active  # t.me/TheVenomXD flags.23?true call_not_empty
        self.noforwards = noforwards  # t.me/TheVenomXD flags.25?true id
        self.admin_rights = admin_rights  # t.me/TheVenomXD flags.14?ChatAdminRights default_banned_rights

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Chat":
        
        flags = TLObject.read(b)
        
        left = True if flags & (1 << 2) else False
        call_active = True if flags & (1 << 23) else False
        noforwards = True if flags & (1 << 25) else False
        title = TLObject.read(b)
        
        participants_count = TLObject.read(b)
        
        version = TLObject.read(b)
        
        admin_rights = TLObject.read(b) if flags & (1 << 14) else None
        
        return Chat(flags=flags, title=title, participants_count=participants_count, version=version, left=left, call_active=call_active, noforwards=noforwards, admin_rights=admin_rights)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.title.write())
        
        b.write(self.participants_count.write())
        
        b.write(self.version.write())
        
        if self.admin_rights is not None:
            b.write(self.admin_rights.write())
        
        return b.getvalue()
