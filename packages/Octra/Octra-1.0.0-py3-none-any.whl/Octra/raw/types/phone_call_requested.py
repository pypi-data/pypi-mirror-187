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


class PhoneCallRequested(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.PhoneCall`.

    Details:
        - Layer: ``151``
        - ID: ``14B0ED0C``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD video <Octra.raw.base.# t.me/TheVenomXD video>`):
            N/A

        id (:obj:`long access_hash <Octra.raw.base.long access_hash>`):
            N/A

        date (:obj:`int admin_id <Octra.raw.base.int admin_id>`):
            N/A

        participant_id (:obj:`long g_a_hash <Octra.raw.base.long g_a_hash>`):
            N/A

        protocol (:obj:`PhoneCallProtocol  <Octra.raw.base.PhoneCallProtocol >`):
            N/A

    """

    __slots__: List[str] = ["flags", "id", "date", "participant_id", "protocol"]

    ID = 0x14b0ed0c
    QUALNAME = "types.PhoneCallRequested"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD video", id: "raw.base.long access_hash", date: "raw.base.int admin_id", participant_id: "raw.base.long g_a_hash", protocol: "raw.base.PhoneCallProtocol ") -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD video
        self.id = id  # t.me/TheVenomXD long access_hash
        self.date = date  # t.me/TheVenomXD int admin_id
        self.participant_id = participant_id  # t.me/TheVenomXD long g_a_hash
        self.protocol = protocol  # t.me/TheVenomXD PhoneCallProtocol 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PhoneCallRequested":
        
        flags = TLObject.read(b)
        
        id = TLObject.read(b)
        
        date = TLObject.read(b)
        
        participant_id = TLObject.read(b)
        
        protocol = TLObject.read(b)
        
        return PhoneCallRequested(flags=flags, id=id, date=date, participant_id=participant_id, protocol=protocol)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.id.write())
        
        b.write(self.date.write())
        
        b.write(self.participant_id.write())
        
        b.write(self.protocol.write())
        
        return b.getvalue()
