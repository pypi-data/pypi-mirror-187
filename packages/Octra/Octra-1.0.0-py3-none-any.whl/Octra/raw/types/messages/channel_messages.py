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


class ChannelMessages(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.messages.Messages`.

    Details:
        - Layer: ``151``
        - ID: ``C776BA4E``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD inexact <Octra.raw.base.# t.me/TheVenomXD inexact>`):
            N/A

        pts (:obj:`int count <Octra.raw.base.int count>`):
            N/A

        topics (List of :obj:`ForumTopic> chat <Octra.raw.base.ForumTopic> chat>`):
            N/A

        users (List of :obj:`User> <Octra.raw.base.User>>`):
            N/A

        offset_id_offset (:obj:`int messages <Octra.raw.base.int messages>`, *optional*):
            N/A

    Functions:
        This object can be returned by 13 functions.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetMessages
            messages.GetHistory
            messages.Search
            messages.SearchGlobal
            messages.GetUnreadMentions
            messages.GetRecentLocations
            messages.GetScheduledHistory
            messages.GetScheduledMessages
            messages.GetReplies
            messages.GetUnreadReactions
            messages.SearchSentMedia
            channels.GetMessages
            stats.GetMessagePublicForwards
    """

    __slots__: List[str] = ["flags", "pts", "topics", "users", "offset_id_offset"]

    ID = 0xc776ba4e
    QUALNAME = "types.messages.ChannelMessages"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD inexact", pts: "raw.base.int count", topics: List["raw.base.ForumTopic> chat"], users: List["raw.base.User>"], offset_id_offset: "raw.base.int messages" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD inexact
        self.pts = pts  # t.me/TheVenomXD int count
        self.topics = topics  # t.me/TheVenomXD Vector<ForumTopic> chats
        self.users = users  # t.me/TheVenomXD Vector<User> 
        self.offset_id_offset = offset_id_offset  # t.me/TheVenomXD flags.2?int messages

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelMessages":
        
        flags = TLObject.read(b)
        
        pts = TLObject.read(b)
        
        offset_id_offset = Int.read(b) if flags & (1 << 2) else None
        topics = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return ChannelMessages(flags=flags, pts=pts, topics=topics, users=users, offset_id_offset=offset_id_offset)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.pts.write())
        
        if self.offset_id_offset is not None:
            b.write(Int(self.offset_id_offset))
        
        b.write(Vector(self.topics))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
