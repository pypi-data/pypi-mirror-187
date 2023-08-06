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


class TranslateText(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``24CE6DEE``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD peer <Octra.raw.base.# t.me/TheVenomXD peer>`):
            N/A

        msg_id (:obj:`int text <Octra.raw.base.int text>`, *optional*):
            N/A

        from_lang (:obj:`string to_lang <Octra.raw.base.string to_lang>`, *optional*):
            N/A

    Returns:
        :obj:`messages.TranslatedText <Octra.raw.base.messages.TranslatedText>`
    """

    __slots__: List[str] = ["flags", "msg_id", "from_lang"]

    ID = 0x24ce6dee
    QUALNAME = "functions.messages.TranslateText"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD peer", msg_id: "raw.base.int text" = None, from_lang: "raw.base.string to_lang" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD peer
        self.msg_id = msg_id  # t.me/TheVenomXD flags.0?int text
        self.from_lang = from_lang  # t.me/TheVenomXD flags.2?string to_lang

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TranslateText":
        
        flags = TLObject.read(b)
        
        msg_id = Int.read(b) if flags & (1 << 0) else None
        from_lang = String.read(b) if flags & (1 << 2) else None
        return TranslateText(flags=flags, msg_id=msg_id, from_lang=from_lang)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.msg_id is not None:
            b.write(Int(self.msg_id))
        
        if self.from_lang is not None:
            b.write(String(self.from_lang))
        
        return b.getvalue()
