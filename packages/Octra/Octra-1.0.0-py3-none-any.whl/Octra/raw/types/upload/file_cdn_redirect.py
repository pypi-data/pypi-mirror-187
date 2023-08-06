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


class FileCdnRedirect(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.upload.File`.

    Details:
        - Layer: ``151``
        - ID: ``F18CDA44``

    Parameters:
        octra_dc_id_ (:obj:`int file_token <Octra.raw.base.int file_token>`):
            N/A

        encryption_key (:obj:`bytes encryption_iv <Octra.raw.base.bytes encryption_iv>`):
            N/A

        file_hashes (List of :obj:`FileHash> <Octra.raw.base.FileHash>>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            upload.GetFile
    """

    __slots__: List[str] = ["octra_dc_id_", "encryption_key", "file_hashes"]

    ID = 0xf18cda44
    QUALNAME = "types.upload.FileCdnRedirect"

    def __init__(self, *, octra_dc_id_: "raw.base.int file_token", encryption_key: "raw.base.bytes encryption_iv", file_hashes: List["raw.base.FileHash>"]) -> None:
        self.octra_dc_id_ = octra_dc_id_  # t.me/TheVenomXD int file_token
        self.encryption_key = encryption_key  # t.me/TheVenomXD bytes encryption_iv
        self.file_hashes = file_hashes  # t.me/TheVenomXD Vector<FileHash> 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "FileCdnRedirect":
        # t.me/TheVenomXD No flags
        
        octra_dc_id_ = TLObject.read(b)
        
        encryption_key = TLObject.read(b)
        
        file_hashes = TLObject.read(b)
        
        return FileCdnRedirect(octra_dc_id_=octra_dc_id_, encryption_key=encryption_key, file_hashes=file_hashes)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # t.me/TheVenomXD No flags
        
        b.write(self.octra_dc_id_.write())
        
        b.write(self.encryption_key.write())
        
        b.write(Vector(self.file_hashes))
        
        return b.getvalue()
