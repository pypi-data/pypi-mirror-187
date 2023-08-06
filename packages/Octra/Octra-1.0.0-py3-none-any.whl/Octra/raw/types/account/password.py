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


class Password(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.account.Password`.

    Details:
        - Layer: ``151``
        - ID: ``957B50FB``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD has_recovery <Octra.raw.base.# t.me/TheVenomXD has_recovery>`):
            N/A

        new_secure_algo (:obj:`SecurePasswordKdfAlgo secure_random <Octra.raw.base.SecurePasswordKdfAlgo secure_random>`):
            N/A

        has_secure_values (:obj:`true has_password <Octra.raw.base.true has_password>`, *optional*):
            N/A

        current_algo (:obj:`PasswordKdfAlgo srp_B <Octra.raw.base.PasswordKdfAlgo srp_B>`, *optional*):
            N/A

        srp_id (:obj:`long hint <Octra.raw.base.long hint>`, *optional*):
            N/A

        email_unconfirmed_pattern (:obj:`string new_algo <Octra.raw.base.string new_algo>`, *optional*):
            N/A

        pending_reset_date (:obj:`int login_email_pattern <Octra.raw.base.int login_email_pattern>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetPassword
    """

    __slots__: List[str] = ["flags", "new_secure_algo", "has_secure_values", "current_algo", "srp_id", "email_unconfirmed_pattern", "pending_reset_date"]

    ID = 0x957b50fb
    QUALNAME = "types.account.Password"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD has_recovery", new_secure_algo: "raw.base.SecurePasswordKdfAlgo secure_random", has_secure_values: "raw.base.true has_password" = None, current_algo: "raw.base.PasswordKdfAlgo srp_B" = None, srp_id: "raw.base.long hint" = None, email_unconfirmed_pattern: "raw.base.string new_algo" = None, pending_reset_date: "raw.base.int login_email_pattern" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD has_recovery
        self.new_secure_algo = new_secure_algo  # t.me/TheVenomXD SecurePasswordKdfAlgo secure_random
        self.has_secure_values = has_secure_values  # t.me/TheVenomXD flags.1?true has_password
        self.current_algo = current_algo  # t.me/TheVenomXD flags.2?PasswordKdfAlgo srp_B
        self.srp_id = srp_id  # t.me/TheVenomXD flags.2?long hint
        self.email_unconfirmed_pattern = email_unconfirmed_pattern  # t.me/TheVenomXD flags.4?string new_algo
        self.pending_reset_date = pending_reset_date  # t.me/TheVenomXD flags.5?int login_email_pattern

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Password":
        
        flags = TLObject.read(b)
        
        has_secure_values = True if flags & (1 << 1) else False
        current_algo = TLObject.read(b) if flags & (1 << 2) else None
        
        srp_id = Long.read(b) if flags & (1 << 2) else None
        email_unconfirmed_pattern = String.read(b) if flags & (1 << 4) else None
        new_secure_algo = TLObject.read(b)
        
        pending_reset_date = Int.read(b) if flags & (1 << 5) else None
        return Password(flags=flags, new_secure_algo=new_secure_algo, has_secure_values=has_secure_values, current_algo=current_algo, srp_id=srp_id, email_unconfirmed_pattern=email_unconfirmed_pattern, pending_reset_date=pending_reset_date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.current_algo is not None:
            b.write(self.current_algo.write())
        
        if self.srp_id is not None:
            b.write(Long(self.srp_id))
        
        if self.email_unconfirmed_pattern is not None:
            b.write(String(self.email_unconfirmed_pattern))
        
        b.write(self.new_secure_algo.write())
        
        if self.pending_reset_date is not None:
            b.write(Int(self.pending_reset_date))
        
        return b.getvalue()
