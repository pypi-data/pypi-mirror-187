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


class WebPage(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.WebPage`.

    Details:
        - Layer: ``151``
        - ID: ``E89C45B2``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD id <Octra.raw.base.# t.me/TheVenomXD id>`):
            N/A

        url (:obj:`string display_url <Octra.raw.base.string display_url>`):
            N/A

        hash (:obj:`int type <Octra.raw.base.int type>`):
            N/A

        site_name (:obj:`string title <Octra.raw.base.string title>`, *optional*):
            N/A

        description (:obj:`string photo <Octra.raw.base.string photo>`, *optional*):
            N/A

        embed_url (:obj:`string embed_type <Octra.raw.base.string embed_type>`, *optional*):
            N/A

        embed_width (:obj:`int embed_height <Octra.raw.base.int embed_height>`, *optional*):
            N/A

        duration (:obj:`int author <Octra.raw.base.int author>`, *optional*):
            N/A

        document (:obj:`Document cached_page <Octra.raw.base.Document cached_page>`, *optional*):
            N/A

        attributes (List of :obj:`WebPageAttribute> <Octra.raw.base.WebPageAttribute>>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetWebPage
    """

    __slots__: List[str] = ["flags", "url", "hash", "site_name", "description", "embed_url", "embed_width", "duration", "document", "attributes"]

    ID = 0xe89c45b2
    QUALNAME = "types.WebPage"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD id", url: "raw.base.string display_url", hash: "raw.base.int type", site_name: "raw.base.string title" = None, description: "raw.base.string photo" = None, embed_url: "raw.base.string embed_type" = None, embed_width: "raw.base.int embed_height" = None, duration: "raw.base.int author" = None, document: "raw.base.Document cached_page" = None, attributes: Optional[List["raw.base.WebPageAttribute>"]] = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD id
        self.url = url  # t.me/TheVenomXD string display_url
        self.hash = hash  # t.me/TheVenomXD int type
        self.site_name = site_name  # t.me/TheVenomXD flags.1?string title
        self.description = description  # t.me/TheVenomXD flags.3?string photo
        self.embed_url = embed_url  # t.me/TheVenomXD flags.5?string embed_type
        self.embed_width = embed_width  # t.me/TheVenomXD flags.6?int embed_height
        self.duration = duration  # t.me/TheVenomXD flags.7?int author
        self.document = document  # t.me/TheVenomXD flags.9?Document cached_page
        self.attributes = attributes  # t.me/TheVenomXD flags.12?Vector<WebPageAttribute> 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "WebPage":
        
        flags = TLObject.read(b)
        
        url = TLObject.read(b)
        
        hash = TLObject.read(b)
        
        site_name = String.read(b) if flags & (1 << 1) else None
        description = String.read(b) if flags & (1 << 3) else None
        embed_url = String.read(b) if flags & (1 << 5) else None
        embed_width = Int.read(b) if flags & (1 << 6) else None
        duration = Int.read(b) if flags & (1 << 7) else None
        document = TLObject.read(b) if flags & (1 << 9) else None
        
        attributes = TLObject.read(b) if flags & (1 << 12) else []
        
        return WebPage(flags=flags, url=url, hash=hash, site_name=site_name, description=description, embed_url=embed_url, embed_width=embed_width, duration=duration, document=document, attributes=attributes)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.url.write())
        
        b.write(self.hash.write())
        
        if self.site_name is not None:
            b.write(String(self.site_name))
        
        if self.description is not None:
            b.write(String(self.description))
        
        if self.embed_url is not None:
            b.write(String(self.embed_url))
        
        if self.embed_width is not None:
            b.write(Int(self.embed_width))
        
        if self.duration is not None:
            b.write(Int(self.duration))
        
        if self.document is not None:
            b.write(self.document.write())
        
        if self.attributes is not None:
            b.write(Vector(self.attributes))
        
        return b.getvalue()
