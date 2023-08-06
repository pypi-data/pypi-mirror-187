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


class ChatInviteImporter(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.ChatInviteImporter`.

    Details:
        - Layer: ``151``
        - ID: ``8C5ADFD9``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD requested <Octra.raw.base.# t.me/TheVenomXD requested>`):
            N/A

        octra_user_id (:obj:`long date <Octra.raw.base.long date>`):
            N/A

        about (:obj:`string approved_by <Octra.raw.base.string approved_by>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "octra_user_id", "about"]

    ID = 0x8c5adfd9
    QUALNAME = "types.ChatInviteImporter"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD requested", octra_user_id: "raw.base.long date", about: "raw.base.string approved_by" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD requested
        self.octra_user_id = octra_user_id  # t.me/TheVenomXD long date
        self.about = about  # t.me/TheVenomXD flags.2?string approved_by

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChatInviteImporter":
        
        flags = TLObject.read(b)
        
        octra_user_id = TLObject.read(b)
        
        about = String.read(b) if flags & (1 << 2) else None
        return ChatInviteImporter(flags=flags, octra_user_id=octra_user_id, about=about)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.octra_user_id.write())
        
        if self.about is not None:
            b.write(String(self.about))
        
        return b.getvalue()
