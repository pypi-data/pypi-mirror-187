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


class EncryptedChatRequested(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.EncryptedChat`.

    Details:
        - Layer: ``151``
        - ID: ``48F1D94C``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD folder_id <Octra.raw.base.# t.me/TheVenomXD folder_id>`):
            N/A

        id (:obj:`int access_hash <Octra.raw.base.int access_hash>`):
            N/A

        date (:obj:`int admin_id <Octra.raw.base.int admin_id>`):
            N/A

        participant_id (:obj:`long g_a <Octra.raw.base.long g_a>`):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            messages.RequestEncryption
            messages.AcceptEncryption
    """

    __slots__: List[str] = ["flags", "id", "date", "participant_id"]

    ID = 0x48f1d94c
    QUALNAME = "types.EncryptedChatRequested"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD folder_id", id: "raw.base.int access_hash", date: "raw.base.int admin_id", participant_id: "raw.base.long g_a") -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD folder_id
        self.id = id  # t.me/TheVenomXD int access_hash
        self.date = date  # t.me/TheVenomXD int admin_id
        self.participant_id = participant_id  # t.me/TheVenomXD long g_a

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EncryptedChatRequested":
        
        flags = TLObject.read(b)
        
        id = TLObject.read(b)
        
        date = TLObject.read(b)
        
        participant_id = TLObject.read(b)
        
        return EncryptedChatRequested(flags=flags, id=id, date=date, participant_id=participant_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.id.write())
        
        b.write(self.date.write())
        
        b.write(self.participant_id.write())
        
        return b.getvalue()
