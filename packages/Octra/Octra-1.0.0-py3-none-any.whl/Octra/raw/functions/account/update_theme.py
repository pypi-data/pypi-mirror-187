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


class UpdateTheme(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``2BF40CCC``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD format <Octra.raw.base.# t.me/TheVenomXD format>`):
            N/A

        theme (:obj:`InputTheme slug <Octra.raw.base.InputTheme slug>`):
            N/A

        title (:obj:`string document <Octra.raw.base.string document>`, *optional*):
            N/A

        settings (List of :obj:`InputThemeSettings> <Octra.raw.base.InputThemeSettings>>`, *optional*):
            N/A

    Returns:
        :obj:`Theme <Octra.raw.base.Theme>`
    """

    __slots__: List[str] = ["flags", "theme", "title", "settings"]

    ID = 0x2bf40ccc
    QUALNAME = "functions.account.UpdateTheme"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD format", theme: "raw.base.InputTheme slug", title: "raw.base.string document" = None, settings: Optional[List["raw.base.InputThemeSettings>"]] = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD format
        self.theme = theme  # t.me/TheVenomXD InputTheme slug
        self.title = title  # t.me/TheVenomXD flags.1?string document
        self.settings = settings  # t.me/TheVenomXD flags.3?Vector<InputThemeSettings> 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateTheme":
        
        flags = TLObject.read(b)
        
        theme = TLObject.read(b)
        
        title = String.read(b) if flags & (1 << 1) else None
        settings = TLObject.read(b) if flags & (1 << 3) else []
        
        return UpdateTheme(flags=flags, theme=theme, title=title, settings=settings)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.theme.write())
        
        if self.title is not None:
            b.write(String(self.title))
        
        if self.settings is not None:
            b.write(Vector(self.settings))
        
        return b.getvalue()
