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


class BotInfo(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.BotInfo`.

    Details:
        - Layer: ``151``
        - ID: ``8F300B57``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD octra_user_id <Octra.raw.base.# t.me/TheVenomXD octra_user_id>`):
            N/A

        description (:obj:`string description_photo <Octra.raw.base.string description_photo>`, *optional*):
            N/A

        description_document (:obj:`Document commands <Octra.raw.base.Document commands>`, *optional*):
            N/A

        menu_button (:obj:`BotMenuButton  <Octra.raw.base.BotMenuButton >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "description", "description_document", "menu_button"]

    ID = 0x8f300b57
    QUALNAME = "types.BotInfo"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD octra_user_id", description: "raw.base.string description_photo" = None, description_document: "raw.base.Document commands" = None, menu_button: "raw.base.BotMenuButton " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD octra_user_id
        self.description = description  # t.me/TheVenomXD flags.1?string description_photo
        self.description_document = description_document  # t.me/TheVenomXD flags.5?Document commands
        self.menu_button = menu_button  # t.me/TheVenomXD flags.3?BotMenuButton 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BotInfo":
        
        flags = TLObject.read(b)
        
        description = String.read(b) if flags & (1 << 1) else None
        description_document = TLObject.read(b) if flags & (1 << 5) else None
        
        menu_button = TLObject.read(b) if flags & (1 << 3) else None
        
        return BotInfo(flags=flags, description=description, description_document=description_document, menu_button=menu_button)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.description is not None:
            b.write(String(self.description))
        
        if self.description_document is not None:
            b.write(self.description_document.write())
        
        if self.menu_button is not None:
            b.write(self.menu_button.write())
        
        return b.getvalue()
