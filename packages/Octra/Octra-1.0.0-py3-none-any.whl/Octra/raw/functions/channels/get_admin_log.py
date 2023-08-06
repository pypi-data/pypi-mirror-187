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


class GetAdminLog(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``33DDF480``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD channel <Octra.raw.base.# t.me/TheVenomXD channel>`):
            N/A

        q (:obj:`string events_Flow <Octra.raw.base.string events_Flow>`):
            N/A

        min_id (:obj:`long limit <Octra.raw.base.long limit>`):
            N/A

        admins (List of :obj:`InputUser> max_i <Octra.raw.base.InputUser> max_i>`, *optional*):
            N/A

    Returns:
        :obj:`channels.AdminLogResults <Octra.raw.base.channels.AdminLogResults>`
    """

    __slots__: List[str] = ["flags", "q", "min_id", "admins"]

    ID = 0x33ddf480
    QUALNAME = "functions.channels.GetAdminLog"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD channel", q: "raw.base.string events_Flow", min_id: "raw.base.long limit", admins: Optional[List["raw.base.InputUser> max_i"]] = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD channel
        self.q = q  # t.me/TheVenomXD string events_Flow
        self.min_id = min_id  # t.me/TheVenomXD long limit
        self.admins = admins  # t.me/TheVenomXD flags.1?Vector<InputUser> max_id

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetAdminLog":
        
        flags = TLObject.read(b)
        
        q = TLObject.read(b)
        
        admins = TLObject.read(b) if flags & (1 << 1) else []
        
        min_id = TLObject.read(b)
        
        return GetAdminLog(flags=flags, q=q, min_id=min_id, admins=admins)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.q.write())
        
        if self.admins is not None:
            b.write(Vector(self.admins))
        
        b.write(self.min_id.write())
        
        return b.getvalue()
