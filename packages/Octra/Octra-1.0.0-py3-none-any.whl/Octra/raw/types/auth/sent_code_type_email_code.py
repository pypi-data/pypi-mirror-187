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


class SentCodeTypeEmailCode(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.auth.SentCodeType`.

    Details:
        - Layer: ``151``
        - ID: ``5A159841``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD apple_signin_allowed <Octra.raw.base.# t.me/TheVenomXD apple_signin_allowed>`):
            N/A

        length (:obj:`int next_phone_login_date <Octra.raw.base.int next_phone_login_date>`):
            N/A

        google_signin_allowed (:obj:`true email_pattern <Octra.raw.base.true email_pattern>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "length", "google_signin_allowed"]

    ID = 0x5a159841
    QUALNAME = "types.auth.SentCodeTypeEmailCode"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD apple_signin_allowed", length: "raw.base.int next_phone_login_date", google_signin_allowed: "raw.base.true email_pattern" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD apple_signin_allowed
        self.length = length  # t.me/TheVenomXD int next_phone_login_date
        self.google_signin_allowed = google_signin_allowed  # t.me/TheVenomXD flags.1?true email_pattern

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SentCodeTypeEmailCode":
        
        flags = TLObject.read(b)
        
        google_signin_allowed = True if flags & (1 << 1) else False
        length = TLObject.read(b)
        
        return SentCodeTypeEmailCode(flags=flags, length=length, google_signin_allowed=google_signin_allowed)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.length.write())
        
        return b.getvalue()
