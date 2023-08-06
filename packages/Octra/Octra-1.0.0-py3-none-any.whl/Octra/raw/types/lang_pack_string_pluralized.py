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


class LangPackStringPluralized(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.LangPackString`.

    Details:
        - Layer: ``151``
        - ID: ``6C47AC9F``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD key <Octra.raw.base.# t.me/TheVenomXD key>`):
            N/A

        zero_value (:obj:`string one_value <Octra.raw.base.string one_value>`, *optional*):
            N/A

        two_value (:obj:`string few_value <Octra.raw.base.string few_value>`, *optional*):
            N/A

        many_value (:obj:`string other_value <Octra.raw.base.string other_value>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            langpack.GetStrings
    """

    __slots__: List[str] = ["flags", "zero_value", "two_value", "many_value"]

    ID = 0x6c47ac9f
    QUALNAME = "types.LangPackStringPluralized"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD key", zero_value: "raw.base.string one_value" = None, two_value: "raw.base.string few_value" = None, many_value: "raw.base.string other_value" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD key
        self.zero_value = zero_value  # t.me/TheVenomXD flags.0?string one_value
        self.two_value = two_value  # t.me/TheVenomXD flags.2?string few_value
        self.many_value = many_value  # t.me/TheVenomXD flags.4?string other_value

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "LangPackStringPluralized":
        
        flags = TLObject.read(b)
        
        zero_value = String.read(b) if flags & (1 << 0) else None
        two_value = String.read(b) if flags & (1 << 2) else None
        many_value = String.read(b) if flags & (1 << 4) else None
        return LangPackStringPluralized(flags=flags, zero_value=zero_value, two_value=two_value, many_value=many_value)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.zero_value is not None:
            b.write(String(self.zero_value))
        
        if self.two_value is not None:
            b.write(String(self.two_value))
        
        if self.many_value is not None:
            b.write(String(self.many_value))
        
        return b.getvalue()
