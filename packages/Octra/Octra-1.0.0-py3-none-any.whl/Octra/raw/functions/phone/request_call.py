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


class RequestCall(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``42FF96ED``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD video <Octra.raw.base.# t.me/TheVenomXD video>`):
            N/A

        octra_user_id (:obj:`InputUser random_id <Octra.raw.base.InputUser random_id>`):
            N/A

        g_a_hash (:obj:`bytes protocol <Octra.raw.base.bytes protocol>`):
            N/A

    Returns:
        :obj:`phone.PhoneCall <Octra.raw.base.phone.PhoneCall>`
    """

    __slots__: List[str] = ["flags", "octra_user_id", "g_a_hash"]

    ID = 0x42ff96ed
    QUALNAME = "functions.phone.RequestCall"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD video", octra_user_id: "raw.base.InputUser random_id", g_a_hash: "raw.base.bytes protocol") -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD video
        self.octra_user_id = octra_user_id  # t.me/TheVenomXD InputUser random_id
        self.g_a_hash = g_a_hash  # t.me/TheVenomXD bytes protocol

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "RequestCall":
        
        flags = TLObject.read(b)
        
        octra_user_id = TLObject.read(b)
        
        g_a_hash = TLObject.read(b)
        
        return RequestCall(flags=flags, octra_user_id=octra_user_id, g_a_hash=g_a_hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.octra_user_id.write())
        
        b.write(self.g_a_hash.write())
        
        return b.getvalue()
