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


class AppUpdate(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.help.AppUpdate`.

    Details:
        - Layer: ``151``
        - ID: ``CCBBCE30``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD can_not_skip <Octra.raw.base.# t.me/TheVenomXD can_not_skip>`):
            N/A

        id (:obj:`int version <Octra.raw.base.int version>`):
            N/A

        text (:obj:`string entities <Octra.raw.base.string entities>`):
            N/A

        document (:obj:`Document url <Octra.raw.base.Document url>`, *optional*):
            N/A

        sticker (:obj:`Document  <Octra.raw.base.Document >`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            help.GetAppUpdate
    """

    __slots__: List[str] = ["flags", "id", "text", "document", "sticker"]

    ID = 0xccbbce30
    QUALNAME = "types.help.AppUpdate"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD can_not_skip", id: "raw.base.int version", text: "raw.base.string entities", document: "raw.base.Document url" = None, sticker: "raw.base.Document " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD can_not_skip
        self.id = id  # t.me/TheVenomXD int version
        self.text = text  # t.me/TheVenomXD string entities
        self.document = document  # t.me/TheVenomXD flags.1?Document url
        self.sticker = sticker  # t.me/TheVenomXD flags.3?Document 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AppUpdate":
        
        flags = TLObject.read(b)
        
        id = TLObject.read(b)
        
        text = TLObject.read(b)
        
        document = TLObject.read(b) if flags & (1 << 1) else None
        
        sticker = TLObject.read(b) if flags & (1 << 3) else None
        
        return AppUpdate(flags=flags, id=id, text=text, document=document, sticker=sticker)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.id.write())
        
        b.write(self.text.write())
        
        if self.document is not None:
            b.write(self.document.write())
        
        if self.sticker is not None:
            b.write(self.sticker.write())
        
        return b.getvalue()
