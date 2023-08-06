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


class GetForumTopics(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``DE560D1``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD channel <Octra.raw.base.# t.me/TheVenomXD channel>`):
            N/A

        offset_id (:obj:`int offset_topic <Octra.raw.base.int offset_topic>`):
            N/A

        limit (:obj:`int  <Octra.raw.base.int >`):
            N/A

        q (:obj:`string offset_date <Octra.raw.base.string offset_date>`, *optional*):
            N/A

    Returns:
        :obj:`messages.ForumTopics <Octra.raw.base.messages.ForumTopics>`
    """

    __slots__: List[str] = ["flags", "offset_id", "limit", "q"]

    ID = 0xde560d1
    QUALNAME = "functions.channels.GetForumTopics"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD channel", offset_id: "raw.base.int offset_topic", limit: "raw.base.int ", q: "raw.base.string offset_date" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD channel
        self.offset_id = offset_id  # t.me/TheVenomXD int offset_topic
        self.limit = limit  # t.me/TheVenomXD int 
        self.q = q  # t.me/TheVenomXD flags.0?string offset_date

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetForumTopics":
        
        flags = TLObject.read(b)
        
        q = String.read(b) if flags & (1 << 0) else None
        offset_id = TLObject.read(b)
        
        limit = TLObject.read(b)
        
        return GetForumTopics(flags=flags, offset_id=offset_id, limit=limit, q=q)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.q is not None:
            b.write(String(self.q))
        
        b.write(self.offset_id.write())
        
        b.write(self.limit.write())
        
        return b.getvalue()
