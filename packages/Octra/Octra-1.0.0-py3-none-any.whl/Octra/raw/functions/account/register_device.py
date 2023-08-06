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


class RegisterDevice(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``EC86017A``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD no_muted <Octra.raw.base.# t.me/TheVenomXD no_muted>`):
            N/A

        token_type (:obj:`int token <Octra.raw.base.int token>`):
            N/A

        app_sandbox (:obj:`Bool secret <Octra.raw.base.Bool secret>`):
            N/A

        other_uids (List of :obj:`long> <Octra.raw.base.long>>`):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["flags", "token_type", "app_sandbox", "other_uids"]

    ID = 0xec86017a
    QUALNAME = "functions.account.RegisterDevice"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD no_muted", token_type: "raw.base.int token", app_sandbox: "raw.base.Bool secret", other_uids: List["raw.base.long>"]) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD no_muted
        self.token_type = token_type  # t.me/TheVenomXD int token
        self.app_sandbox = app_sandbox  # t.me/TheVenomXD Bool secret
        self.other_uids = other_uids  # t.me/TheVenomXD Vector<long> 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "RegisterDevice":
        
        flags = TLObject.read(b)
        
        token_type = TLObject.read(b)
        
        app_sandbox = TLObject.read(b)
        
        other_uids = TLObject.read(b)
        
        return RegisterDevice(flags=flags, token_type=token_type, app_sandbox=app_sandbox, other_uids=other_uids)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.token_type.write())
        
        b.write(self.app_sandbox.write())
        
        b.write(Vector(self.other_uids))
        
        return b.getvalue()
