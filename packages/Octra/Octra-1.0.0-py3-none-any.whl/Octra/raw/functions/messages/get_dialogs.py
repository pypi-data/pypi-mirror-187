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


class GetDialogs(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``A0F4CB4F``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD exclude_pinned <Octra.raw.base.# t.me/TheVenomXD exclude_pinned>`):
            N/A

        offset_id (:obj:`int offset_peer <Octra.raw.base.int offset_peer>`):
            N/A

        limit (:obj:`int hash <Octra.raw.base.int hash>`):
            N/A

        folder_id (:obj:`int offset_date <Octra.raw.base.int offset_date>`, *optional*):
            N/A

    Returns:
        :obj:`messages.Dialogs <Octra.raw.base.messages.Dialogs>`
    """

    __slots__: List[str] = ["flags", "offset_id", "limit", "folder_id"]

    ID = 0xa0f4cb4f
    QUALNAME = "functions.messages.GetDialogs"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD exclude_pinned", offset_id: "raw.base.int offset_peer", limit: "raw.base.int hash", folder_id: "raw.base.int offset_date" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD exclude_pinned
        self.offset_id = offset_id  # t.me/TheVenomXD int offset_peer
        self.limit = limit  # t.me/TheVenomXD int hash
        self.folder_id = folder_id  # t.me/TheVenomXD flags.1?int offset_date

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetDialogs":
        
        flags = TLObject.read(b)
        
        folder_id = Int.read(b) if flags & (1 << 1) else None
        offset_id = TLObject.read(b)
        
        limit = TLObject.read(b)
        
        return GetDialogs(flags=flags, offset_id=offset_id, limit=limit, folder_id=folder_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.folder_id is not None:
            b.write(Int(self.folder_id))
        
        b.write(self.offset_id.write())
        
        b.write(self.limit.write())
        
        return b.getvalue()
