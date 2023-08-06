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


class AuthorizationForm(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.account.AuthorizationForm`.

    Details:
        - Layer: ``151``
        - ID: ``AD2E1CD8``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD required_types <Octra.raw.base.# t.me/TheVenomXD required_types>`):
            N/A

        values (List of :obj:`SecureValue> error <Octra.raw.base.SecureValue> error>`):
            N/A

        users (List of :obj:`User> privacy_policy_ur <Octra.raw.base.User> privacy_policy_ur>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetAuthorizationForm
    """

    __slots__: List[str] = ["flags", "values", "users"]

    ID = 0xad2e1cd8
    QUALNAME = "types.account.AuthorizationForm"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD required_types", values: List["raw.base.SecureValue> error"], users: List["raw.base.User> privacy_policy_ur"]) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD required_types
        self.values = values  # t.me/TheVenomXD Vector<SecureValue> errors
        self.users = users  # t.me/TheVenomXD Vector<User> privacy_policy_url

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AuthorizationForm":
        
        flags = TLObject.read(b)
        
        values = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return AuthorizationForm(flags=flags, values=values, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(Vector(self.values))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
