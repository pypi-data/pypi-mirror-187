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


class ChatInviteExported(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.ExportedChatInvite`.

    Details:
        - Layer: ``151``
        - ID: ``AB4A819``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD revoked <Octra.raw.base.# t.me/TheVenomXD revoked>`):
            N/A

        link (:obj:`string admin_id <Octra.raw.base.string admin_id>`):
            N/A

        date (:obj:`int start_date <Octra.raw.base.int start_date>`):
            N/A

        permanent (:obj:`true request_needed <Octra.raw.base.true request_needed>`, *optional*):
            N/A

        expire_date (:obj:`int usage_limit <Octra.raw.base.int usage_limit>`, *optional*):
            N/A

        usage (:obj:`int requested <Octra.raw.base.int requested>`, *optional*):
            N/A

        title (:obj:`string  <Octra.raw.base.string >`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            messages.ExportChatInvite
    """

    __slots__: List[str] = ["flags", "link", "date", "permanent", "expire_date", "usage", "title"]

    ID = 0xab4a819
    QUALNAME = "types.ChatInviteExported"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD revoked", link: "raw.base.string admin_id", date: "raw.base.int start_date", permanent: "raw.base.true request_needed" = None, expire_date: "raw.base.int usage_limit" = None, usage: "raw.base.int requested" = None, title: "raw.base.string " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD revoked
        self.link = link  # t.me/TheVenomXD string admin_id
        self.date = date  # t.me/TheVenomXD int start_date
        self.permanent = permanent  # t.me/TheVenomXD flags.5?true request_needed
        self.expire_date = expire_date  # t.me/TheVenomXD flags.1?int usage_limit
        self.usage = usage  # t.me/TheVenomXD flags.3?int requested
        self.title = title  # t.me/TheVenomXD flags.8?string 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChatInviteExported":
        
        flags = TLObject.read(b)
        
        permanent = True if flags & (1 << 5) else False
        link = TLObject.read(b)
        
        date = TLObject.read(b)
        
        expire_date = Int.read(b) if flags & (1 << 1) else None
        usage = Int.read(b) if flags & (1 << 3) else None
        title = String.read(b) if flags & (1 << 8) else None
        return ChatInviteExported(flags=flags, link=link, date=date, permanent=permanent, expire_date=expire_date, usage=usage, title=title)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.link.write())
        
        b.write(self.date.write())
        
        if self.expire_date is not None:
            b.write(Int(self.expire_date))
        
        if self.usage is not None:
            b.write(Int(self.usage))
        
        if self.title is not None:
            b.write(String(self.title))
        
        return b.getvalue()
