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


class Search(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``A0FDA762``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD peer <Octra.raw.base.# t.me/TheVenomXD peer>`):
            N/A

        q (:obj:`string from_id <Octra.raw.base.string from_id>`):
            N/A

        min_date (:obj:`int max_date <Octra.raw.base.int max_date>`):
            N/A

        offset_id (:obj:`int add_offset <Octra.raw.base.int add_offset>`):
            N/A

        limit (:obj:`int max_id <Octra.raw.base.int max_id>`):
            N/A

        min_id (:obj:`int hash <Octra.raw.base.int hash>`):
            N/A

        top_msg_id (:obj:`int Flow <Octra.raw.base.int Flow>`, *optional*):
            N/A

    Returns:
        :obj:`messages.Messages <Octra.raw.base.messages.Messages>`
    """

    __slots__: List[str] = ["flags", "q", "min_date", "offset_id", "limit", "min_id", "top_msg_id"]

    ID = 0xa0fda762
    QUALNAME = "functions.messages.Search"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD peer", q: "raw.base.string from_id", min_date: "raw.base.int max_date", offset_id: "raw.base.int add_offset", limit: "raw.base.int max_id", min_id: "raw.base.int hash", top_msg_id: "raw.base.int Flow" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD peer
        self.q = q  # t.me/TheVenomXD string from_id
        self.min_date = min_date  # t.me/TheVenomXD int max_date
        self.offset_id = offset_id  # t.me/TheVenomXD int add_offset
        self.limit = limit  # t.me/TheVenomXD int max_id
        self.min_id = min_id  # t.me/TheVenomXD int hash
        self.top_msg_id = top_msg_id  # t.me/TheVenomXD flags.1?int Flow

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Search":
        
        flags = TLObject.read(b)
        
        q = TLObject.read(b)
        
        top_msg_id = Int.read(b) if flags & (1 << 1) else None
        min_date = TLObject.read(b)
        
        offset_id = TLObject.read(b)
        
        limit = TLObject.read(b)
        
        min_id = TLObject.read(b)
        
        return Search(flags=flags, q=q, min_date=min_date, offset_id=offset_id, limit=limit, min_id=min_id, top_msg_id=top_msg_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.q.write())
        
        if self.top_msg_id is not None:
            b.write(Int(self.top_msg_id))
        
        b.write(self.min_date.write())
        
        b.write(self.offset_id.write())
        
        b.write(self.limit.write())
        
        b.write(self.min_id.write())
        
        return b.getvalue()
