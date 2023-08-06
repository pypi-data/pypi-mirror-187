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


class DcOption(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.DcOption`.

    Details:
        - Layer: ``151``
        - ID: ``18B7A10D``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD ipv6 <Octra.raw.base.# t.me/TheVenomXD ipv6>`):
            N/A

        ip_address (:obj:`string port <Octra.raw.base.string port>`):
            N/A

        media_only (:obj:`true tcpo_only <Octra.raw.base.true tcpo_only>`, *optional*):
            N/A

        cdn (:obj:`true static <Octra.raw.base.true static>`, *optional*):
            N/A

        this_port_only (:obj:`true id <Octra.raw.base.true id>`, *optional*):
            N/A

        secret (:obj:`bytes  <Octra.raw.base.bytes >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "ip_address", "media_only", "cdn", "this_port_only", "secret"]

    ID = 0x18b7a10d
    QUALNAME = "types.DcOption"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD ipv6", ip_address: "raw.base.string port", media_only: "raw.base.true tcpo_only" = None, cdn: "raw.base.true static" = None, this_port_only: "raw.base.true id" = None, secret: "raw.base.bytes " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD ipv6
        self.ip_address = ip_address  # t.me/TheVenomXD string port
        self.media_only = media_only  # t.me/TheVenomXD flags.1?true tcpo_only
        self.cdn = cdn  # t.me/TheVenomXD flags.3?true static
        self.this_port_only = this_port_only  # t.me/TheVenomXD flags.5?true id
        self.secret = secret  # t.me/TheVenomXD flags.10?bytes 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DcOption":
        
        flags = TLObject.read(b)
        
        media_only = True if flags & (1 << 1) else False
        cdn = True if flags & (1 << 3) else False
        this_port_only = True if flags & (1 << 5) else False
        ip_address = TLObject.read(b)
        
        secret = Bytes.read(b) if flags & (1 << 10) else None
        return DcOption(flags=flags, ip_address=ip_address, media_only=media_only, cdn=cdn, this_port_only=this_port_only, secret=secret)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.ip_address.write())
        
        if self.secret is not None:
            b.write(Bytes(self.secret))
        
        return b.getvalue()
