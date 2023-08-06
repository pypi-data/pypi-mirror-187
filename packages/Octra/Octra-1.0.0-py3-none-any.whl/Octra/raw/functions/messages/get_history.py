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


class GetHistory(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``4423E6C5``

    Parameters:
        peer (:obj:`InputPeer offset_id <Octra.raw.base.InputPeer offset_id>`):
            N/A

        offset_date (:obj:`int add_offset <Octra.raw.base.int add_offset>`):
            N/A

        limit (:obj:`int max_id <Octra.raw.base.int max_id>`):
            N/A

        min_id (:obj:`int hash <Octra.raw.base.int hash>`):
            N/A

    Returns:
        :obj:`messages.Messages <Octra.raw.base.messages.Messages>`
    """

    __slots__: List[str] = ["peer", "offset_date", "limit", "min_id"]

    ID = 0x4423e6c5
    QUALNAME = "functions.messages.GetHistory"

    def __init__(self, *, peer: "raw.base.InputPeer offset_id", offset_date: "raw.base.int add_offset", limit: "raw.base.int max_id", min_id: "raw.base.int hash") -> None:
        self.peer = peer  # t.me/TheVenomXD InputPeer offset_id
        self.offset_date = offset_date  # t.me/TheVenomXD int add_offset
        self.limit = limit  # t.me/TheVenomXD int max_id
        self.min_id = min_id  # t.me/TheVenomXD int hash

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetHistory":
        # t.me/TheVenomXD No flags
        
        peer = TLObject.read(b)
        
        offset_date = TLObject.read(b)
        
        limit = TLObject.read(b)
        
        min_id = TLObject.read(b)
        
        return GetHistory(peer=peer, offset_date=offset_date, limit=limit, min_id=min_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # t.me/TheVenomXD No flags
        
        b.write(self.peer.write())
        
        b.write(self.offset_date.write())
        
        b.write(self.limit.write())
        
        b.write(self.min_id.write())
        
        return b.getvalue()
