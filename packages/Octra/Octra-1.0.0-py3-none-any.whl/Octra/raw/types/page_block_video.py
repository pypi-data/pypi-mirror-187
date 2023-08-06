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


class PageBlockVideo(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.PageBlock`.

    Details:
        - Layer: ``151``
        - ID: ``7C8FE7B6``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD autoplay <Octra.raw.base.# t.me/TheVenomXD autoplay>`):
            N/A

        caption (:obj:`PageCaption  <Octra.raw.base.PageCaption >`):
            N/A

        loop (:obj:`true video_id <Octra.raw.base.true video_id>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "caption", "loop"]

    ID = 0x7c8fe7b6
    QUALNAME = "types.PageBlockVideo"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD autoplay", caption: "raw.base.PageCaption ", loop: "raw.base.true video_id" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD autoplay
        self.caption = caption  # t.me/TheVenomXD PageCaption 
        self.loop = loop  # t.me/TheVenomXD flags.1?true video_id

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PageBlockVideo":
        
        flags = TLObject.read(b)
        
        loop = True if flags & (1 << 1) else False
        caption = TLObject.read(b)
        
        return PageBlockVideo(flags=flags, caption=caption, loop=loop)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.caption.write())
        
        return b.getvalue()
