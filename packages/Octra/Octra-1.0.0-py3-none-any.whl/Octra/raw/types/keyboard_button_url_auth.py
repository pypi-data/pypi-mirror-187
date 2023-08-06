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


class KeyboardButtonUrlAuth(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.KeyboardButton`.

    Details:
        - Layer: ``151``
        - ID: ``10B78D29``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD text <Octra.raw.base.# t.me/TheVenomXD text>`):
            N/A

        button_id (:obj:`int  <Octra.raw.base.int >`):
            N/A

        fwd_text (:obj:`string url <Octra.raw.base.string url>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "button_id", "fwd_text"]

    ID = 0x10b78d29
    QUALNAME = "types.KeyboardButtonUrlAuth"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD text", button_id: "raw.base.int ", fwd_text: "raw.base.string url" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD text
        self.button_id = button_id  # t.me/TheVenomXD int 
        self.fwd_text = fwd_text  # t.me/TheVenomXD flags.0?string url

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "KeyboardButtonUrlAuth":
        
        flags = TLObject.read(b)
        
        fwd_text = String.read(b) if flags & (1 << 0) else None
        button_id = TLObject.read(b)
        
        return KeyboardButtonUrlAuth(flags=flags, button_id=button_id, fwd_text=fwd_text)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.fwd_text is not None:
            b.write(String(self.fwd_text))
        
        b.write(self.button_id.write())
        
        return b.getvalue()
