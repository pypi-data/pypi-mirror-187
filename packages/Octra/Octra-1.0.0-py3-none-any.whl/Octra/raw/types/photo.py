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


class Photo(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Photo`.

    Details:
        - Layer: ``151``
        - ID: ``FB197A65``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD has_stickers <Octra.raw.base.# t.me/TheVenomXD has_stickers>`):
            N/A

        id (:obj:`long access_hash <Octra.raw.base.long access_hash>`):
            N/A

        file_reference (:obj:`bytes date <Octra.raw.base.bytes date>`):
            N/A

        sizes (List of :obj:`PhotoSize> video_size <Octra.raw.base.PhotoSize> video_size>`):
            N/A

        octra_dc_id_ (:obj:`int  <Octra.raw.base.int >`):
            N/A

    """

    __slots__: List[str] = ["flags", "id", "file_reference", "sizes", "octra_dc_id_"]

    ID = 0xfb197a65
    QUALNAME = "types.Photo"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD has_stickers", id: "raw.base.long access_hash", file_reference: "raw.base.bytes date", sizes: List["raw.base.PhotoSize> video_size"], octra_dc_id_: "raw.base.int ") -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD has_stickers
        self.id = id  # t.me/TheVenomXD long access_hash
        self.file_reference = file_reference  # t.me/TheVenomXD bytes date
        self.sizes = sizes  # t.me/TheVenomXD Vector<PhotoSize> video_sizes
        self.octra_dc_id_ = octra_dc_id_  # t.me/TheVenomXD int 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Photo":
        
        flags = TLObject.read(b)
        
        id = TLObject.read(b)
        
        file_reference = TLObject.read(b)
        
        sizes = TLObject.read(b)
        
        octra_dc_id_ = TLObject.read(b)
        
        return Photo(flags=flags, id=id, file_reference=file_reference, sizes=sizes, octra_dc_id_=octra_dc_id_)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.id.write())
        
        b.write(self.file_reference.write())
        
        b.write(Vector(self.sizes))
        
        b.write(self.octra_dc_id_.write())
        
        return b.getvalue()
