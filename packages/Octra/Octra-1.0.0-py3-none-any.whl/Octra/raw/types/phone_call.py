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


class PhoneCall(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.PhoneCall`.

    Details:
        - Layer: ``151``
        - ID: ``967F7C67``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD p2p_allowed <Octra.raw.base.# t.me/TheVenomXD p2p_allowed>`):
            N/A

        access_hash (:obj:`long date <Octra.raw.base.long date>`):
            N/A

        admin_id (:obj:`long participant_id <Octra.raw.base.long participant_id>`):
            N/A

        g_a_or_b (:obj:`bytes key_fingerprint <Octra.raw.base.bytes key_fingerprint>`):
            N/A

        protocol (:obj:`PhoneCallProtocol connections <Octra.raw.base.PhoneCallProtocol connections>`):
            N/A

        start_date (:obj:`int  <Octra.raw.base.int >`):
            N/A

        video (:obj:`true id <Octra.raw.base.true id>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "access_hash", "admin_id", "g_a_or_b", "protocol", "start_date", "video"]

    ID = 0x967f7c67
    QUALNAME = "types.PhoneCall"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD p2p_allowed", access_hash: "raw.base.long date", admin_id: "raw.base.long participant_id", g_a_or_b: "raw.base.bytes key_fingerprint", protocol: "raw.base.PhoneCallProtocol connections", start_date: "raw.base.int ", video: "raw.base.true id" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD p2p_allowed
        self.access_hash = access_hash  # t.me/TheVenomXD long date
        self.admin_id = admin_id  # t.me/TheVenomXD long participant_id
        self.g_a_or_b = g_a_or_b  # t.me/TheVenomXD bytes key_fingerprint
        self.protocol = protocol  # t.me/TheVenomXD PhoneCallProtocol connections
        self.start_date = start_date  # t.me/TheVenomXD int 
        self.video = video  # t.me/TheVenomXD flags.6?true id

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PhoneCall":
        
        flags = TLObject.read(b)
        
        video = True if flags & (1 << 6) else False
        access_hash = TLObject.read(b)
        
        admin_id = TLObject.read(b)
        
        g_a_or_b = TLObject.read(b)
        
        protocol = TLObject.read(b)
        
        start_date = TLObject.read(b)
        
        return PhoneCall(flags=flags, access_hash=access_hash, admin_id=admin_id, g_a_or_b=g_a_or_b, protocol=protocol, start_date=start_date, video=video)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.access_hash.write())
        
        b.write(self.admin_id.write())
        
        b.write(self.g_a_or_b.write())
        
        b.write(self.protocol.write())
        
        b.write(self.start_date.write())
        
        return b.getvalue()
