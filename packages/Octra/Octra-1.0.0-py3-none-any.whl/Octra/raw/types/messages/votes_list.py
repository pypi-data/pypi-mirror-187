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


class VotesList(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.messages.VotesList`.

    Details:
        - Layer: ``151``
        - ID: ``823F649``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD count <Octra.raw.base.# t.me/TheVenomXD count>`):
            N/A

        votes (List of :obj:`MessageUserVote> user <Octra.raw.base.MessageUserVote> user>`):
            N/A

        next_offset (:obj:`string  <Octra.raw.base.string >`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetPollVotes
    """

    __slots__: List[str] = ["flags", "votes", "next_offset"]

    ID = 0x823f649
    QUALNAME = "types.messages.VotesList"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD count", votes: List["raw.base.MessageUserVote> user"], next_offset: "raw.base.string " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD count
        self.votes = votes  # t.me/TheVenomXD Vector<MessageUserVote> users
        self.next_offset = next_offset  # t.me/TheVenomXD flags.0?string 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "VotesList":
        
        flags = TLObject.read(b)
        
        votes = TLObject.read(b)
        
        next_offset = String.read(b) if flags & (1 << 0) else None
        return VotesList(flags=flags, votes=votes, next_offset=next_offset)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(Vector(self.votes))
        
        if self.next_offset is not None:
            b.write(String(self.next_offset))
        
        return b.getvalue()
