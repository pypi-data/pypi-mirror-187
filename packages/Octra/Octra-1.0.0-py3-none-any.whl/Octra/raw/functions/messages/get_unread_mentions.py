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


class GetUnreadMentions(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``F107E790``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD peer <Octra.raw.base.# t.me/TheVenomXD peer>`):
            N/A

        add_offset (:obj:`int limit <Octra.raw.base.int limit>`):
            N/A

        max_id (:obj:`int min_id <Octra.raw.base.int min_id>`):
            N/A

        top_msg_id (:obj:`int offset_id <Octra.raw.base.int offset_id>`, *optional*):
            N/A

    Returns:
        :obj:`messages.Messages <Octra.raw.base.messages.Messages>`
    """

    __slots__: List[str] = ["flags", "add_offset", "max_id", "top_msg_id"]

    ID = 0xf107e790
    QUALNAME = "functions.messages.GetUnreadMentions"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD peer", add_offset: "raw.base.int limit", max_id: "raw.base.int min_id", top_msg_id: "raw.base.int offset_id" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD peer
        self.add_offset = add_offset  # t.me/TheVenomXD int limit
        self.max_id = max_id  # t.me/TheVenomXD int min_id
        self.top_msg_id = top_msg_id  # t.me/TheVenomXD flags.0?int offset_id

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetUnreadMentions":
        
        flags = TLObject.read(b)
        
        top_msg_id = Int.read(b) if flags & (1 << 0) else None
        add_offset = TLObject.read(b)
        
        max_id = TLObject.read(b)
        
        return GetUnreadMentions(flags=flags, add_offset=add_offset, max_id=max_id, top_msg_id=top_msg_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.top_msg_id is not None:
            b.write(Int(self.top_msg_id))
        
        b.write(self.add_offset.write())
        
        b.write(self.max_id.write())
        
        return b.getvalue()
