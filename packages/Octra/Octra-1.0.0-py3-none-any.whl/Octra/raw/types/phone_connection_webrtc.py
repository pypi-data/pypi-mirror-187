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


class PhoneConnectionWebrtc(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.PhoneConnection`.

    Details:
        - Layer: ``151``
        - ID: ``635FE375``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD turn <Octra.raw.base.# t.me/TheVenomXD turn>`):
            N/A

        ip (:obj:`string ipv6 <Octra.raw.base.string ipv6>`):
            N/A

        port (:obj:`int username <Octra.raw.base.int username>`):
            N/A

        password (:obj:`string  <Octra.raw.base.string >`):
            N/A

        stun (:obj:`true id <Octra.raw.base.true id>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "ip", "port", "password", "stun"]

    ID = 0x635fe375
    QUALNAME = "types.PhoneConnectionWebrtc"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD turn", ip: "raw.base.string ipv6", port: "raw.base.int username", password: "raw.base.string ", stun: "raw.base.true id" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD turn
        self.ip = ip  # t.me/TheVenomXD string ipv6
        self.port = port  # t.me/TheVenomXD int username
        self.password = password  # t.me/TheVenomXD string 
        self.stun = stun  # t.me/TheVenomXD flags.1?true id

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PhoneConnectionWebrtc":
        
        flags = TLObject.read(b)
        
        stun = True if flags & (1 << 1) else False
        ip = TLObject.read(b)
        
        port = TLObject.read(b)
        
        password = TLObject.read(b)
        
        return PhoneConnectionWebrtc(flags=flags, ip=ip, port=port, password=password, stun=stun)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.ip.write())
        
        b.write(self.port.write())
        
        b.write(self.password.write())
        
        return b.getvalue()
