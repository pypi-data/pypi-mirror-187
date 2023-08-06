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


class Theme(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Theme`.

    Details:
        - Layer: ``151``
        - ID: ``A00E67D6``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD creator <Octra.raw.base.# t.me/TheVenomXD creator>`):
            N/A

        id (:obj:`long access_hash <Octra.raw.base.long access_hash>`):
            N/A

        slug (:obj:`string title <Octra.raw.base.string title>`):
            N/A

        default (:obj:`true for_chat <Octra.raw.base.true for_chat>`, *optional*):
            N/A

        document (:obj:`Document settings <Octra.raw.base.Document settings>`, *optional*):
            N/A

        emoticon (:obj:`string installs_count <Octra.raw.base.string installs_count>`, *optional*):
            N/A

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            account.CreateTheme
            account.UpdateTheme
            account.GetTheme
    """

    __slots__: List[str] = ["flags", "id", "slug", "default", "document", "emoticon"]

    ID = 0xa00e67d6
    QUALNAME = "types.Theme"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD creator", id: "raw.base.long access_hash", slug: "raw.base.string title", default: "raw.base.true for_chat" = None, document: "raw.base.Document settings" = None, emoticon: "raw.base.string installs_count" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD creator
        self.id = id  # t.me/TheVenomXD long access_hash
        self.slug = slug  # t.me/TheVenomXD string title
        self.default = default  # t.me/TheVenomXD flags.1?true for_chat
        self.document = document  # t.me/TheVenomXD flags.2?Document settings
        self.emoticon = emoticon  # t.me/TheVenomXD flags.6?string installs_count

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Theme":
        
        flags = TLObject.read(b)
        
        default = True if flags & (1 << 1) else False
        id = TLObject.read(b)
        
        slug = TLObject.read(b)
        
        document = TLObject.read(b) if flags & (1 << 2) else None
        
        emoticon = String.read(b) if flags & (1 << 6) else None
        return Theme(flags=flags, id=id, slug=slug, default=default, document=document, emoticon=emoticon)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.id.write())
        
        b.write(self.slug.write())
        
        if self.document is not None:
            b.write(self.document.write())
        
        if self.emoticon is not None:
            b.write(String(self.emoticon))
        
        return b.getvalue()
