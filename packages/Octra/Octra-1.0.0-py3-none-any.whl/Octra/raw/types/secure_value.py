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


class SecureValue(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.SecureValue`.

    Details:
        - Layer: ``151``
        - ID: ``187FA0CA``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD type <Octra.raw.base.# t.me/TheVenomXD type>`):
            N/A

        data (:obj:`SecureData front_side <Octra.raw.base.SecureData front_side>`, *optional*):
            N/A

        reverse_side (:obj:`SecureFile selfie <Octra.raw.base.SecureFile selfie>`, *optional*):
            N/A

        translation (List of :obj:`SecureFile> file <Octra.raw.base.SecureFile> file>`, *optional*):
            N/A

        plain_data (:obj:`SecurePlainData hash <Octra.raw.base.SecurePlainData hash>`, *optional*):
            N/A

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetAllSecureValues
            account.GetSecureValue
            account.SaveSecureValue
    """

    __slots__: List[str] = ["flags", "data", "reverse_side", "translation", "plain_data"]

    ID = 0x187fa0ca
    QUALNAME = "types.SecureValue"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD type", data: "raw.base.SecureData front_side" = None, reverse_side: "raw.base.SecureFile selfie" = None, translation: Optional[List["raw.base.SecureFile> file"]] = None, plain_data: "raw.base.SecurePlainData hash" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD type
        self.data = data  # t.me/TheVenomXD flags.0?SecureData front_side
        self.reverse_side = reverse_side  # t.me/TheVenomXD flags.2?SecureFile selfie
        self.translation = translation  # t.me/TheVenomXD flags.6?Vector<SecureFile> files
        self.plain_data = plain_data  # t.me/TheVenomXD flags.5?SecurePlainData hash

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SecureValue":
        
        flags = TLObject.read(b)
        
        data = TLObject.read(b) if flags & (1 << 0) else None
        
        reverse_side = TLObject.read(b) if flags & (1 << 2) else None
        
        translation = TLObject.read(b) if flags & (1 << 6) else []
        
        plain_data = TLObject.read(b) if flags & (1 << 5) else None
        
        return SecureValue(flags=flags, data=data, reverse_side=reverse_side, translation=translation, plain_data=plain_data)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.data is not None:
            b.write(self.data.write())
        
        if self.reverse_side is not None:
            b.write(self.reverse_side.write())
        
        if self.translation is not None:
            b.write(Vector(self.translation))
        
        if self.plain_data is not None:
            b.write(self.plain_data.write())
        
        return b.getvalue()
