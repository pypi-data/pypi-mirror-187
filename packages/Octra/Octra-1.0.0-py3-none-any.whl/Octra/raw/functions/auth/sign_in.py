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


class SignIn(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``8D52A951``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD phone_number <Octra.raw.base.# t.me/TheVenomXD phone_number>`):
            N/A

        phone_code_hash (:obj:`string phone_code <Octra.raw.base.string phone_code>`):
            N/A

        email_verification (:obj:`EmailVerification  <Octra.raw.base.EmailVerification >`, *optional*):
            N/A

    Returns:
        :obj:`auth.Authorization <Octra.raw.base.auth.Authorization>`
    """

    __slots__: List[str] = ["flags", "phone_code_hash", "email_verification"]

    ID = 0x8d52a951
    QUALNAME = "functions.auth.SignIn"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD phone_number", phone_code_hash: "raw.base.string phone_code", email_verification: "raw.base.EmailVerification " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD phone_number
        self.phone_code_hash = phone_code_hash  # t.me/TheVenomXD string phone_code
        self.email_verification = email_verification  # t.me/TheVenomXD flags.1?EmailVerification 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SignIn":
        
        flags = TLObject.read(b)
        
        phone_code_hash = TLObject.read(b)
        
        email_verification = TLObject.read(b) if flags & (1 << 1) else None
        
        return SignIn(flags=flags, phone_code_hash=phone_code_hash, email_verification=email_verification)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.phone_code_hash.write())
        
        if self.email_verification is not None:
            b.write(self.email_verification.write())
        
        return b.getvalue()
