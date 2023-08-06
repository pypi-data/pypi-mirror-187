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


class WallPaperSettings(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.WallPaperSettings`.

    Details:
        - Layer: ``151``
        - ID: ``1DC1BCA4``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD blur <Octra.raw.base.# t.me/TheVenomXD blur>`):
            N/A

        motion (:obj:`true background_color <Octra.raw.base.true background_color>`, *optional*):
            N/A

        second_background_color (:obj:`int third_background_color <Octra.raw.base.int third_background_color>`, *optional*):
            N/A

        fourth_background_color (:obj:`int intensity <Octra.raw.base.int intensity>`, *optional*):
            N/A

        rotation (:obj:`int  <Octra.raw.base.int >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "motion", "second_background_color", "fourth_background_color", "rotation"]

    ID = 0x1dc1bca4
    QUALNAME = "types.WallPaperSettings"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD blur", motion: "raw.base.true background_color" = None, second_background_color: "raw.base.int third_background_color" = None, fourth_background_color: "raw.base.int intensity" = None, rotation: "raw.base.int " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD blur
        self.motion = motion  # t.me/TheVenomXD flags.2?true background_color
        self.second_background_color = second_background_color  # t.me/TheVenomXD flags.4?int third_background_color
        self.fourth_background_color = fourth_background_color  # t.me/TheVenomXD flags.6?int intensity
        self.rotation = rotation  # t.me/TheVenomXD flags.4?int 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "WallPaperSettings":
        
        flags = TLObject.read(b)
        
        motion = True if flags & (1 << 2) else False
        second_background_color = Int.read(b) if flags & (1 << 4) else None
        fourth_background_color = Int.read(b) if flags & (1 << 6) else None
        rotation = Int.read(b) if flags & (1 << 4) else None
        return WallPaperSettings(flags=flags, motion=motion, second_background_color=second_background_color, fourth_background_color=fourth_background_color, rotation=rotation)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.second_background_color is not None:
            b.write(Int(self.second_background_color))
        
        if self.fourth_background_color is not None:
            b.write(Int(self.fourth_background_color))
        
        if self.rotation is not None:
            b.write(Int(self.rotation))
        
        return b.getvalue()
