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


class BindOctraAuthKeyInner(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.BindAuthKeyInner`.

    Details:
        - Layer: ``151``
        - ID: ``75A3F765``

    Parameters:
        nonce (:obj:`long temp_octra_auth_key_id <Octra.raw.base.long temp_octra_auth_key_id>`):
            N/A

        perm_octra_auth_key_id (:obj:`long temp_session_id <Octra.raw.base.long temp_session_id>`):
            N/A

        expires_at (:obj:`int  <Octra.raw.base.int >`):
            N/A

    """

    __slots__: List[str] = ["nonce", "perm_octra_auth_key_id", "expires_at"]

    ID = 0x75a3f765
    QUALNAME = "types.BindOctraAuthKeyInner"

    def __init__(self, *, nonce: "raw.base.long temp_octra_auth_key_id", perm_octra_auth_key_id: "raw.base.long temp_session_id", expires_at: "raw.base.int ") -> None:
        self.nonce = nonce  # t.me/TheVenomXD long temp_octra_auth_key_id
        self.perm_octra_auth_key_id = perm_octra_auth_key_id  # t.me/TheVenomXD long temp_session_id
        self.expires_at = expires_at  # t.me/TheVenomXD int 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BindOctraAuthKeyInner":
        # t.me/TheVenomXD No flags
        
        nonce = TLObject.read(b)
        
        perm_octra_auth_key_id = TLObject.read(b)
        
        expires_at = TLObject.read(b)
        
        return BindOctraAuthKeyInner(nonce=nonce, perm_octra_auth_key_id=perm_octra_auth_key_id, expires_at=expires_at)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # t.me/TheVenomXD No flags
        
        b.write(self.nonce.write())
        
        b.write(self.perm_octra_auth_key_id.write())
        
        b.write(self.expires_at.write())
        
        return b.getvalue()
