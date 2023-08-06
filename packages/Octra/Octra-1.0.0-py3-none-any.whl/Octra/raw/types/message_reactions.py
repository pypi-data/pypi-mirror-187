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


class MessageReactions(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.MessageReactions`.

    Details:
        - Layer: ``151``
        - ID: ``4F2B9479``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD min <Octra.raw.base.# t.me/TheVenomXD min>`):
            N/A

        can_see_list (:obj:`true results <Octra.raw.base.true results>`, *optional*):
            N/A

        recent_reactions (List of :obj:`MessagePeerReaction> <Octra.raw.base.MessagePeerReaction>>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "can_see_list", "recent_reactions"]

    ID = 0x4f2b9479
    QUALNAME = "types.MessageReactions"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD min", can_see_list: "raw.base.true results" = None, recent_reactions: Optional[List["raw.base.MessagePeerReaction>"]] = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD min
        self.can_see_list = can_see_list  # t.me/TheVenomXD flags.2?true results
        self.recent_reactions = recent_reactions  # t.me/TheVenomXD flags.1?Vector<MessagePeerReaction> 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageReactions":
        
        flags = TLObject.read(b)
        
        can_see_list = True if flags & (1 << 2) else False
        recent_reactions = TLObject.read(b) if flags & (1 << 1) else []
        
        return MessageReactions(flags=flags, can_see_list=can_see_list, recent_reactions=recent_reactions)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.recent_reactions is not None:
            b.write(Vector(self.recent_reactions))
        
        return b.getvalue()
