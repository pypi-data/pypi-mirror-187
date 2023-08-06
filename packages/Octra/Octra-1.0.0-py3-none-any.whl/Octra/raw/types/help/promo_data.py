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


class PromoData(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.help.PromoData`.

    Details:
        - Layer: ``151``
        - ID: ``8C39793F``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD proxy <Octra.raw.base.# t.me/TheVenomXD proxy>`):
            N/A

        expires (:obj:`int peer <Octra.raw.base.int peer>`):
            N/A

        chats (List of :obj:`Chat> user <Octra.raw.base.Chat> user>`):
            N/A

        psa_type (:obj:`string psa_message <Octra.raw.base.string psa_message>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            help.GetPromoData
    """

    __slots__: List[str] = ["flags", "expires", "chats", "psa_type"]

    ID = 0x8c39793f
    QUALNAME = "types.help.PromoData"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD proxy", expires: "raw.base.int peer", chats: List["raw.base.Chat> user"], psa_type: "raw.base.string psa_message" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD proxy
        self.expires = expires  # t.me/TheVenomXD int peer
        self.chats = chats  # t.me/TheVenomXD Vector<Chat> users
        self.psa_type = psa_type  # t.me/TheVenomXD flags.1?string psa_message

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PromoData":
        
        flags = TLObject.read(b)
        
        expires = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        psa_type = String.read(b) if flags & (1 << 1) else None
        return PromoData(flags=flags, expires=expires, chats=chats, psa_type=psa_type)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.expires.write())
        
        b.write(Vector(self.chats))
        
        if self.psa_type is not None:
            b.write(String(self.psa_type))
        
        return b.getvalue()
