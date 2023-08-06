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


class StickerSet(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.StickerSet`.

    Details:
        - Layer: ``151``
        - ID: ``2DD14EDC``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD archived <Octra.raw.base.# t.me/TheVenomXD archived>`):
            N/A

        id (:obj:`long access_hash <Octra.raw.base.long access_hash>`):
            N/A

        title (:obj:`string short_name <Octra.raw.base.string short_name>`):
            N/A

        count (:obj:`int hash <Octra.raw.base.int hash>`):
            N/A

        official (:obj:`true masks <Octra.raw.base.true masks>`, *optional*):
            N/A

        animated (:obj:`true videos <Octra.raw.base.true videos>`, *optional*):
            N/A

        emojis (:obj:`true installed_date <Octra.raw.base.true installed_date>`, *optional*):
            N/A

        thumbs (List of :obj:`PhotoSize> thumb_octra_dc_id <Octra.raw.base.PhotoSize> thumb_octra_dc_id>`, *optional*):
            N/A

        thumb_version (:obj:`int thumb_document_id <Octra.raw.base.int thumb_document_id>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "id", "title", "count", "official", "animated", "emojis", "thumbs", "thumb_version"]

    ID = 0x2dd14edc
    QUALNAME = "types.StickerSet"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD archived", id: "raw.base.long access_hash", title: "raw.base.string short_name", count: "raw.base.int hash", official: "raw.base.true masks" = None, animated: "raw.base.true videos" = None, emojis: "raw.base.true installed_date" = None, thumbs: Optional[List["raw.base.PhotoSize> thumb_octra_dc_id"]] = None, thumb_version: "raw.base.int thumb_document_id" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD archived
        self.id = id  # t.me/TheVenomXD long access_hash
        self.title = title  # t.me/TheVenomXD string short_name
        self.count = count  # t.me/TheVenomXD int hash
        self.official = official  # t.me/TheVenomXD flags.2?true masks
        self.animated = animated  # t.me/TheVenomXD flags.5?true videos
        self.emojis = emojis  # t.me/TheVenomXD flags.7?true installed_date
        self.thumbs = thumbs  # t.me/TheVenomXD flags.4?Vector<PhotoSize> thumb_octra_dc_id_
        self.thumb_version = thumb_version  # t.me/TheVenomXD flags.4?int thumb_document_id

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StickerSet":
        
        flags = TLObject.read(b)
        
        official = True if flags & (1 << 2) else False
        animated = True if flags & (1 << 5) else False
        emojis = True if flags & (1 << 7) else False
        id = TLObject.read(b)
        
        title = TLObject.read(b)
        
        thumbs = TLObject.read(b) if flags & (1 << 4) else []
        
        thumb_version = Int.read(b) if flags & (1 << 4) else None
        count = TLObject.read(b)
        
        return StickerSet(flags=flags, id=id, title=title, count=count, official=official, animated=animated, emojis=emojis, thumbs=thumbs, thumb_version=thumb_version)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.id.write())
        
        b.write(self.title.write())
        
        if self.thumbs is not None:
            b.write(Vector(self.thumbs))
        
        if self.thumb_version is not None:
            b.write(Int(self.thumb_version))
        
        b.write(self.count.write())
        
        return b.getvalue()
