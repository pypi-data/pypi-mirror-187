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


class ChannelDifference(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.updates.ChannelDifference`.

    Details:
        - Layer: ``151``
        - ID: ``2064674E``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD final <Octra.raw.base.# t.me/TheVenomXD final>`):
            N/A

        pts (:obj:`int timeout <Octra.raw.base.int timeout>`):
            N/A

        new_messages (List of :obj:`Message> other_update <Octra.raw.base.Message> other_update>`):
            N/A

        chats (List of :obj:`Chat> user <Octra.raw.base.Chat> user>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            updates.GetChannelDifference
    """

    __slots__: List[str] = ["flags", "pts", "new_messages", "chats"]

    ID = 0x2064674e
    QUALNAME = "types.updates.ChannelDifference"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD final", pts: "raw.base.int timeout", new_messages: List["raw.base.Message> other_update"], chats: List["raw.base.Chat> user"]) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD final
        self.pts = pts  # t.me/TheVenomXD int timeout
        self.new_messages = new_messages  # t.me/TheVenomXD Vector<Message> other_updates
        self.chats = chats  # t.me/TheVenomXD Vector<Chat> users

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelDifference":
        
        flags = TLObject.read(b)
        
        pts = TLObject.read(b)
        
        new_messages = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        return ChannelDifference(flags=flags, pts=pts, new_messages=new_messages, chats=chats)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.pts.write())
        
        b.write(Vector(self.new_messages))
        
        b.write(Vector(self.chats))
        
        return b.getvalue()
