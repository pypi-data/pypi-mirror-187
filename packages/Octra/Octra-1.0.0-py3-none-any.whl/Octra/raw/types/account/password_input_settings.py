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


class PasswordInputSettings(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.account.PasswordInputSettings`.

    Details:
        - Layer: ``151``
        - ID: ``C23727C9``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD new_algo <Octra.raw.base.# t.me/TheVenomXD new_algo>`):
            N/A

        new_password_hash (:obj:`bytes hint <Octra.raw.base.bytes hint>`, *optional*):
            N/A

        email (:obj:`string new_secure_settings <Octra.raw.base.string new_secure_settings>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "new_password_hash", "email"]

    ID = 0xc23727c9
    QUALNAME = "types.account.PasswordInputSettings"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD new_algo", new_password_hash: "raw.base.bytes hint" = None, email: "raw.base.string new_secure_settings" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD new_algo
        self.new_password_hash = new_password_hash  # t.me/TheVenomXD flags.0?bytes hint
        self.email = email  # t.me/TheVenomXD flags.1?string new_secure_settings

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PasswordInputSettings":
        
        flags = TLObject.read(b)
        
        new_password_hash = Bytes.read(b) if flags & (1 << 0) else None
        email = String.read(b) if flags & (1 << 1) else None
        return PasswordInputSettings(flags=flags, new_password_hash=new_password_hash, email=email)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.new_password_hash is not None:
            b.write(Bytes(self.new_password_hash))
        
        if self.email is not None:
            b.write(String(self.email))
        
        return b.getvalue()
