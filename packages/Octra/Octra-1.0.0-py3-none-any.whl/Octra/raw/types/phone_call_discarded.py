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


class PhoneCallDiscarded(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.PhoneCall`.

    Details:
        - Layer: ``151``
        - ID: ``50CA4DE1``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD need_rating <Octra.raw.base.# t.me/TheVenomXD need_rating>`):
            N/A

        id (:obj:`long reason <Octra.raw.base.long reason>`):
            N/A

        need_debug (:obj:`true video <Octra.raw.base.true video>`, *optional*):
            N/A

        duration (:obj:`int  <Octra.raw.base.int >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "id", "need_debug", "duration"]

    ID = 0x50ca4de1
    QUALNAME = "types.PhoneCallDiscarded"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD need_rating", id: "raw.base.long reason", need_debug: "raw.base.true video" = None, duration: "raw.base.int " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD need_rating
        self.id = id  # t.me/TheVenomXD long reason
        self.need_debug = need_debug  # t.me/TheVenomXD flags.3?true video
        self.duration = duration  # t.me/TheVenomXD flags.1?int 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PhoneCallDiscarded":
        
        flags = TLObject.read(b)
        
        need_debug = True if flags & (1 << 3) else False
        id = TLObject.read(b)
        
        duration = Int.read(b) if flags & (1 << 1) else None
        return PhoneCallDiscarded(flags=flags, id=id, need_debug=need_debug, duration=duration)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.id.write())
        
        if self.duration is not None:
            b.write(Int(self.duration))
        
        return b.getvalue()
