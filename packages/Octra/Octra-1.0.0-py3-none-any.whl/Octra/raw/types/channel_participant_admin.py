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


class ChannelParticipantAdmin(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.ChannelParticipant`.

    Details:
        - Layer: ``151``
        - ID: ``34C3BB53``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD can_edit <Octra.raw.base.# t.me/TheVenomXD can_edit>`):
            N/A

        date (:obj:`int admin_rights <Octra.raw.base.int admin_rights>`):
            N/A

        is_self (:obj:`true octra_user_id <Octra.raw.base.true octra_user_id>`, *optional*):
            N/A

        inviter_id (:obj:`long promoted_by <Octra.raw.base.long promoted_by>`, *optional*):
            N/A

        rank (:obj:`string  <Octra.raw.base.string >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "date", "is_self", "inviter_id", "rank"]

    ID = 0x34c3bb53
    QUALNAME = "types.ChannelParticipantAdmin"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD can_edit", date: "raw.base.int admin_rights", is_self: "raw.base.true octra_user_id" = None, inviter_id: "raw.base.long promoted_by" = None, rank: "raw.base.string " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD can_edit
        self.date = date  # t.me/TheVenomXD int admin_rights
        self.is_self = is_self  # t.me/TheVenomXD flags.1?true octra_user_id
        self.inviter_id = inviter_id  # t.me/TheVenomXD flags.1?long promoted_by
        self.rank = rank  # t.me/TheVenomXD flags.2?string 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelParticipantAdmin":
        
        flags = TLObject.read(b)
        
        is_self = True if flags & (1 << 1) else False
        inviter_id = Long.read(b) if flags & (1 << 1) else None
        date = TLObject.read(b)
        
        rank = String.read(b) if flags & (1 << 2) else None
        return ChannelParticipantAdmin(flags=flags, date=date, is_self=is_self, inviter_id=inviter_id, rank=rank)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.inviter_id is not None:
            b.write(Long(self.inviter_id))
        
        b.write(self.date.write())
        
        if self.rank is not None:
            b.write(String(self.rank))
        
        return b.getvalue()
