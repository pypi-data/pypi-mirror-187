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


class PaExtractableCell(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.PaExtractableCell`.

    Details:
        - Layer: ``151``
        - ID: ``34566B6A``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD header <Octra.raw.base.# t.me/TheVenomXD header>`):
            N/A

        align_center (:obj:`true align_right <Octra.raw.base.true align_right>`, *optional*):
            N/A

        valign_middle (:obj:`true valign_bottom <Octra.raw.base.true valign_bottom>`, *optional*):
            N/A

        text (:obj:`RichText colspan <Octra.raw.base.RichText colspan>`, *optional*):
            N/A

        rowspan (:obj:`int  <Octra.raw.base.int >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "align_center", "valign_middle", "text", "rowspan"]

    ID = 0x34566b6a
    QUALNAME = "types.PaExtractableCell"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD header", align_center: "raw.base.true align_right" = None, valign_middle: "raw.base.true valign_bottom" = None, text: "raw.base.RichText colspan" = None, rowspan: "raw.base.int " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD header
        self.align_center = align_center  # t.me/TheVenomXD flags.3?true align_right
        self.valign_middle = valign_middle  # t.me/TheVenomXD flags.5?true valign_bottom
        self.text = text  # t.me/TheVenomXD flags.7?RichText colspan
        self.rowspan = rowspan  # t.me/TheVenomXD flags.2?int 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PaExtractableCell":
        
        flags = TLObject.read(b)
        
        align_center = True if flags & (1 << 3) else False
        valign_middle = True if flags & (1 << 5) else False
        text = TLObject.read(b) if flags & (1 << 7) else None
        
        rowspan = Int.read(b) if flags & (1 << 2) else None
        return PaExtractableCell(flags=flags, align_center=align_center, valign_middle=valign_middle, text=text, rowspan=rowspan)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.text is not None:
            b.write(self.text.write())
        
        if self.rowspan is not None:
            b.write(Int(self.rowspan))
        
        return b.getvalue()
