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


class ExportChatInvite(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``A02CE5D5``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD legacy_revoke_permanent <Octra.raw.base.# t.me/TheVenomXD legacy_revoke_permanent>`):
            N/A

        request_needed (:obj:`true peer <Octra.raw.base.true peer>`, *optional*):
            N/A

        expire_date (:obj:`int usage_limit <Octra.raw.base.int usage_limit>`, *optional*):
            N/A

        title (:obj:`string  <Octra.raw.base.string >`, *optional*):
            N/A

    Returns:
        :obj:`ExportedChatInvite <Octra.raw.base.ExportedChatInvite>`
    """

    __slots__: List[str] = ["flags", "request_needed", "expire_date", "title"]

    ID = 0xa02ce5d5
    QUALNAME = "functions.messages.ExportChatInvite"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD legacy_revoke_permanent", request_needed: "raw.base.true peer" = None, expire_date: "raw.base.int usage_limit" = None, title: "raw.base.string " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD legacy_revoke_permanent
        self.request_needed = request_needed  # t.me/TheVenomXD flags.3?true peer
        self.expire_date = expire_date  # t.me/TheVenomXD flags.0?int usage_limit
        self.title = title  # t.me/TheVenomXD flags.4?string 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ExportChatInvite":
        
        flags = TLObject.read(b)
        
        request_needed = True if flags & (1 << 3) else False
        expire_date = Int.read(b) if flags & (1 << 0) else None
        title = String.read(b) if flags & (1 << 4) else None
        return ExportChatInvite(flags=flags, request_needed=request_needed, expire_date=expire_date, title=title)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.expire_date is not None:
            b.write(Int(self.expire_date))
        
        if self.title is not None:
            b.write(String(self.title))
        
        return b.getvalue()
