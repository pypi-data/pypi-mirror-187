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


class DeleteHistory(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``B08F922A``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD just_clear <Octra.raw.base.# t.me/TheVenomXD just_clear>`):
            N/A

        max_id (:obj:`int min_date <Octra.raw.base.int min_date>`):
            N/A

        revoke (:obj:`true peer <Octra.raw.base.true peer>`, *optional*):
            N/A

        max_date (:obj:`int  <Octra.raw.base.int >`, *optional*):
            N/A

    Returns:
        :obj:`messages.AffectedHistory <Octra.raw.base.messages.AffectedHistory>`
    """

    __slots__: List[str] = ["flags", "max_id", "revoke", "max_date"]

    ID = 0xb08f922a
    QUALNAME = "functions.messages.DeleteHistory"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD just_clear", max_id: "raw.base.int min_date", revoke: "raw.base.true peer" = None, max_date: "raw.base.int " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD just_clear
        self.max_id = max_id  # t.me/TheVenomXD int min_date
        self.revoke = revoke  # t.me/TheVenomXD flags.1?true peer
        self.max_date = max_date  # t.me/TheVenomXD flags.3?int 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DeleteHistory":
        
        flags = TLObject.read(b)
        
        revoke = True if flags & (1 << 1) else False
        max_id = TLObject.read(b)
        
        max_date = Int.read(b) if flags & (1 << 3) else None
        return DeleteHistory(flags=flags, max_id=max_id, revoke=revoke, max_date=max_date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.max_id.write())
        
        if self.max_date is not None:
            b.write(Int(self.max_date))
        
        return b.getvalue()
