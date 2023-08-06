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


class PageBlockEmbed(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.PageBlock`.

    Details:
        - Layer: ``151``
        - ID: ``A8718DC5``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD full_width <Octra.raw.base.# t.me/TheVenomXD full_width>`):
            N/A

        caption (:obj:`PageCaption  <Octra.raw.base.PageCaption >`):
            N/A

        allow_scrolling (:obj:`true url <Octra.raw.base.true url>`, *optional*):
            N/A

        html (:obj:`string poster_photo_id <Octra.raw.base.string poster_photo_id>`, *optional*):
            N/A

        w (:obj:`int h <Octra.raw.base.int h>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "caption", "allow_scrolling", "html", "w"]

    ID = 0xa8718dc5
    QUALNAME = "types.PageBlockEmbed"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD full_width", caption: "raw.base.PageCaption ", allow_scrolling: "raw.base.true url" = None, html: "raw.base.string poster_photo_id" = None, w: "raw.base.int h" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD full_width
        self.caption = caption  # t.me/TheVenomXD PageCaption 
        self.allow_scrolling = allow_scrolling  # t.me/TheVenomXD flags.3?true url
        self.html = html  # t.me/TheVenomXD flags.2?string poster_photo_id
        self.w = w  # t.me/TheVenomXD flags.5?int h

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PageBlockEmbed":
        
        flags = TLObject.read(b)
        
        allow_scrolling = True if flags & (1 << 3) else False
        html = String.read(b) if flags & (1 << 2) else None
        w = Int.read(b) if flags & (1 << 5) else None
        caption = TLObject.read(b)
        
        return PageBlockEmbed(flags=flags, caption=caption, allow_scrolling=allow_scrolling, html=html, w=w)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.html is not None:
            b.write(String(self.html))
        
        if self.w is not None:
            b.write(Int(self.w))
        
        b.write(self.caption.write())
        
        return b.getvalue()
