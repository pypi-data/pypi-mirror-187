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


class ThemeSettings(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.ThemeSettings`.

    Details:
        - Layer: ``151``
        - ID: ``FA58B6D4``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD message_colors_animated <Octra.raw.base.# t.me/TheVenomXD message_colors_animated>`):
            N/A

        base_theme (:obj:`BaseTheme accent_color <Octra.raw.base.BaseTheme accent_color>`):
            N/A

        outbox_accent_color (:obj:`int message_colors <Octra.raw.base.int message_colors>`, *optional*):
            N/A

        wallpaper (:obj:`WallPaper  <Octra.raw.base.WallPaper >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "base_theme", "outbox_accent_color", "wallpaper"]

    ID = 0xfa58b6d4
    QUALNAME = "types.ThemeSettings"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD message_colors_animated", base_theme: "raw.base.BaseTheme accent_color", outbox_accent_color: "raw.base.int message_colors" = None, wallpaper: "raw.base.WallPaper " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD message_colors_animated
        self.base_theme = base_theme  # t.me/TheVenomXD BaseTheme accent_color
        self.outbox_accent_color = outbox_accent_color  # t.me/TheVenomXD flags.3?int message_colors
        self.wallpaper = wallpaper  # t.me/TheVenomXD flags.1?WallPaper 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ThemeSettings":
        
        flags = TLObject.read(b)
        
        base_theme = TLObject.read(b)
        
        outbox_accent_color = Int.read(b) if flags & (1 << 3) else None
        wallpaper = TLObject.read(b) if flags & (1 << 1) else None
        
        return ThemeSettings(flags=flags, base_theme=base_theme, outbox_accent_color=outbox_accent_color, wallpaper=wallpaper)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.base_theme.write())
        
        if self.outbox_accent_color is not None:
            b.write(Int(self.outbox_accent_color))
        
        if self.wallpaper is not None:
            b.write(self.wallpaper.write())
        
        return b.getvalue()
