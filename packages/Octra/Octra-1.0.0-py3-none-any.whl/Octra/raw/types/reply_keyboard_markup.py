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


class ReplyKeyboardMarkup(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.ReplyMarkup`.

    Details:
        - Layer: ``151``
        - ID: ``85DD99D1``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD resize <Octra.raw.base.# t.me/TheVenomXD resize>`):
            N/A

        single_use (:obj:`true selective <Octra.raw.base.true selective>`, *optional*):
            N/A

        persistent (:obj:`true rows <Octra.raw.base.true rows>`, *optional*):
            N/A

        placeholder (:obj:`string  <Octra.raw.base.string >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "single_use", "persistent", "placeholder"]

    ID = 0x85dd99d1
    QUALNAME = "types.ReplyKeyboardMarkup"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD resize", single_use: "raw.base.true selective" = None, persistent: "raw.base.true rows" = None, placeholder: "raw.base.string " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD resize
        self.single_use = single_use  # t.me/TheVenomXD flags.1?true selective
        self.persistent = persistent  # t.me/TheVenomXD flags.4?true rows
        self.placeholder = placeholder  # t.me/TheVenomXD flags.3?string 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ReplyKeyboardMarkup":
        
        flags = TLObject.read(b)
        
        single_use = True if flags & (1 << 1) else False
        persistent = True if flags & (1 << 4) else False
        placeholder = String.read(b) if flags & (1 << 3) else None
        return ReplyKeyboardMarkup(flags=flags, single_use=single_use, persistent=persistent, placeholder=placeholder)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.placeholder is not None:
            b.write(String(self.placeholder))
        
        return b.getvalue()
