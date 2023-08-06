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


class Document(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Document`.

    Details:
        - Layer: ``151``
        - ID: ``8FD4C4D8``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD id <Octra.raw.base.# t.me/TheVenomXD id>`):
            N/A

        access_hash (:obj:`long file_reference <Octra.raw.base.long file_reference>`):
            N/A

        date (:obj:`int mime_type <Octra.raw.base.int mime_type>`):
            N/A

        size (:obj:`long thumbs <Octra.raw.base.long thumbs>`):
            N/A

        attributes (List of :obj:`DocumentAttribute> <Octra.raw.base.DocumentAttribute>>`):
            N/A

        video_thumbs (List of :obj:`VideoSize> octra_dc_id <Octra.raw.base.VideoSize> octra_dc_id>`, *optional*):
            N/A

    Functions:
        This object can be returned by 4 functions.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            account.UploadTheme
            account.UploadRingtone
            messages.GetDocumentByHash
            messages.GetCustomEmojiDocuments
    """

    __slots__: List[str] = ["flags", "access_hash", "date", "size", "attributes", "video_thumbs"]

    ID = 0x8fd4c4d8
    QUALNAME = "types.Document"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD id", access_hash: "raw.base.long file_reference", date: "raw.base.int mime_type", size: "raw.base.long thumbs", attributes: List["raw.base.DocumentAttribute>"], video_thumbs: Optional[List["raw.base.VideoSize> octra_dc_id"]] = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD id
        self.access_hash = access_hash  # t.me/TheVenomXD long file_reference
        self.date = date  # t.me/TheVenomXD int mime_type
        self.size = size  # t.me/TheVenomXD long thumbs
        self.attributes = attributes  # t.me/TheVenomXD Vector<DocumentAttribute> 
        self.video_thumbs = video_thumbs  # t.me/TheVenomXD flags.1?Vector<VideoSize> octra_dc_id_

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Document":
        
        flags = TLObject.read(b)
        
        access_hash = TLObject.read(b)
        
        date = TLObject.read(b)
        
        size = TLObject.read(b)
        
        video_thumbs = TLObject.read(b) if flags & (1 << 1) else []
        
        attributes = TLObject.read(b)
        
        return Document(flags=flags, access_hash=access_hash, date=date, size=size, attributes=attributes, video_thumbs=video_thumbs)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.access_hash.write())
        
        b.write(self.date.write())
        
        b.write(self.size.write())
        
        if self.video_thumbs is not None:
            b.write(Vector(self.video_thumbs))
        
        b.write(Vector(self.attributes))
        
        return b.getvalue()
