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


class MessageReplyHeader(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.MessageReplyHeader`.

    Details:
        - Layer: ``151``
        - ID: ``A6D57763``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD reply_to_scheduled <Octra.raw.base.# t.me/TheVenomXD reply_to_scheduled>`):
            N/A

        forum_topic (:obj:`true reply_to_msg_id <Octra.raw.base.true reply_to_msg_id>`, *optional*):
            N/A

        reply_to_peer_id (:obj:`Peer reply_to_top_id <Octra.raw.base.Peer reply_to_top_id>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "forum_topic", "reply_to_peer_id"]

    ID = 0xa6d57763
    QUALNAME = "types.MessageReplyHeader"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD reply_to_scheduled", forum_topic: "raw.base.true reply_to_msg_id" = None, reply_to_peer_id: "raw.base.Peer reply_to_top_id" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD reply_to_scheduled
        self.forum_topic = forum_topic  # t.me/TheVenomXD flags.3?true reply_to_msg_id
        self.reply_to_peer_id = reply_to_peer_id  # t.me/TheVenomXD flags.0?Peer reply_to_top_id

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageReplyHeader":
        
        flags = TLObject.read(b)
        
        forum_topic = True if flags & (1 << 3) else False
        reply_to_peer_id = TLObject.read(b) if flags & (1 << 0) else None
        
        return MessageReplyHeader(flags=flags, forum_topic=forum_topic, reply_to_peer_id=reply_to_peer_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.reply_to_peer_id is not None:
            b.write(self.reply_to_peer_id.write())
        
        return b.getvalue()
