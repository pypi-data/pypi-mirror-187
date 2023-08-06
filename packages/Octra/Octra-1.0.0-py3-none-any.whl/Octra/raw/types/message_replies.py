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


class MessageReplies(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.MessageReplies`.

    Details:
        - Layer: ``151``
        - ID: ``83D60FC2``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD comments <Octra.raw.base.# t.me/TheVenomXD comments>`):
            N/A

        replies (:obj:`int replies_pts <Octra.raw.base.int replies_pts>`):
            N/A

        recent_repliers (List of :obj:`Peer> channel_i <Octra.raw.base.Peer> channel_i>`, *optional*):
            N/A

        max_id (:obj:`int read_max_id <Octra.raw.base.int read_max_id>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "replies", "recent_repliers", "max_id"]

    ID = 0x83d60fc2
    QUALNAME = "types.MessageReplies"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD comments", replies: "raw.base.int replies_pts", recent_repliers: Optional[List["raw.base.Peer> channel_i"]] = None, max_id: "raw.base.int read_max_id" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD comments
        self.replies = replies  # t.me/TheVenomXD int replies_pts
        self.recent_repliers = recent_repliers  # t.me/TheVenomXD flags.1?Vector<Peer> channel_id
        self.max_id = max_id  # t.me/TheVenomXD flags.2?int read_max_id

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageReplies":
        
        flags = TLObject.read(b)
        
        replies = TLObject.read(b)
        
        recent_repliers = TLObject.read(b) if flags & (1 << 1) else []
        
        max_id = Int.read(b) if flags & (1 << 2) else None
        return MessageReplies(flags=flags, replies=replies, recent_repliers=recent_repliers, max_id=max_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.replies.write())
        
        if self.recent_repliers is not None:
            b.write(Vector(self.recent_repliers))
        
        if self.max_id is not None:
            b.write(Int(self.max_id))
        
        return b.getvalue()
