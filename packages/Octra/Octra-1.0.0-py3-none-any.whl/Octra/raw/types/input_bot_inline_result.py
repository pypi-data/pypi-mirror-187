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


class InputBotInlineResult(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.InputBotInlineResult`.

    Details:
        - Layer: ``151``
        - ID: ``88BF9319``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD id <Octra.raw.base.# t.me/TheVenomXD id>`):
            N/A

        type (:obj:`string title <Octra.raw.base.string title>`):
            N/A

        send_message (:obj:`InputBotInlineMessage  <Octra.raw.base.InputBotInlineMessage >`):
            N/A

        description (:obj:`string url <Octra.raw.base.string url>`, *optional*):
            N/A

        thumb (:obj:`InputWebDocument content <Octra.raw.base.InputWebDocument content>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "type", "send_message", "description", "thumb"]

    ID = 0x88bf9319
    QUALNAME = "types.InputBotInlineResult"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD id", type: "raw.base.string title", send_message: "raw.base.InputBotInlineMessage ", description: "raw.base.string url" = None, thumb: "raw.base.InputWebDocument content" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD id
        self.type = type  # t.me/TheVenomXD string title
        self.send_message = send_message  # t.me/TheVenomXD InputBotInlineMessage 
        self.description = description  # t.me/TheVenomXD flags.2?string url
        self.thumb = thumb  # t.me/TheVenomXD flags.4?InputWebDocument content

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputBotInlineResult":
        
        flags = TLObject.read(b)
        
        type = TLObject.read(b)
        
        description = String.read(b) if flags & (1 << 2) else None
        thumb = TLObject.read(b) if flags & (1 << 4) else None
        
        send_message = TLObject.read(b)
        
        return InputBotInlineResult(flags=flags, type=type, send_message=send_message, description=description, thumb=thumb)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.type.write())
        
        if self.description is not None:
            b.write(String(self.description))
        
        if self.thumb is not None:
            b.write(self.thumb.write())
        
        b.write(self.send_message.write())
        
        return b.getvalue()
