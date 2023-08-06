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


class PageRelatedArticle(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.PageRelatedArticle`.

    Details:
        - Layer: ``151``
        - ID: ``B390DC08``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD url <Octra.raw.base.# t.me/TheVenomXD url>`):
            N/A

        webpage_id (:obj:`long title <Octra.raw.base.long title>`):
            N/A

        description (:obj:`string photo_id <Octra.raw.base.string photo_id>`, *optional*):
            N/A

        author (:obj:`string published_date <Octra.raw.base.string published_date>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "webpage_id", "description", "author"]

    ID = 0xb390dc08
    QUALNAME = "types.PageRelatedArticle"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD url", webpage_id: "raw.base.long title", description: "raw.base.string photo_id" = None, author: "raw.base.string published_date" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD url
        self.webpage_id = webpage_id  # t.me/TheVenomXD long title
        self.description = description  # t.me/TheVenomXD flags.1?string photo_id
        self.author = author  # t.me/TheVenomXD flags.3?string published_date

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PageRelatedArticle":
        
        flags = TLObject.read(b)
        
        webpage_id = TLObject.read(b)
        
        description = String.read(b) if flags & (1 << 1) else None
        author = String.read(b) if flags & (1 << 3) else None
        return PageRelatedArticle(flags=flags, webpage_id=webpage_id, description=description, author=author)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.webpage_id.write())
        
        if self.description is not None:
            b.write(String(self.description))
        
        if self.author is not None:
            b.write(String(self.author))
        
        return b.getvalue()
