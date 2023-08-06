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


class DocumentAttributeSticker(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.DocumentAttribute`.

    Details:
        - Layer: ``151``
        - ID: ``6319D612``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD mask <Octra.raw.base.# t.me/TheVenomXD mask>`):
            N/A

        alt (:obj:`string stickerset <Octra.raw.base.string stickerset>`):
            N/A

        mask_coords (:obj:`MaskCoords  <Octra.raw.base.MaskCoords >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "alt", "mask_coords"]

    ID = 0x6319d612
    QUALNAME = "types.DocumentAttributeSticker"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD mask", alt: "raw.base.string stickerset", mask_coords: "raw.base.MaskCoords " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD mask
        self.alt = alt  # t.me/TheVenomXD string stickerset
        self.mask_coords = mask_coords  # t.me/TheVenomXD flags.0?MaskCoords 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DocumentAttributeSticker":
        
        flags = TLObject.read(b)
        
        alt = TLObject.read(b)
        
        mask_coords = TLObject.read(b) if flags & (1 << 0) else None
        
        return DocumentAttributeSticker(flags=flags, alt=alt, mask_coords=mask_coords)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.alt.write())
        
        if self.mask_coords is not None:
            b.write(self.mask_coords.write())
        
        return b.getvalue()
