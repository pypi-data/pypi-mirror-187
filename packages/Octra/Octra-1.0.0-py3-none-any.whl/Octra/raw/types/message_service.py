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


class MessageService(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Message`.

    Details:
        - Layer: ``151``
        - ID: ``2B085862``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD out <Octra.raw.base.# t.me/TheVenomXD out>`):
            N/A

        action (:obj:`MessageAction ttl_period <Octra.raw.base.MessageAction ttl_period>`):
            N/A

        mentioned (:obj:`true media_unread <Octra.raw.base.true media_unread>`, *optional*):
            N/A

        silent (:obj:`true post <Octra.raw.base.true post>`, *optional*):
            N/A

        legacy (:obj:`true id <Octra.raw.base.true id>`, *optional*):
            N/A

        from_id (:obj:`Peer peer_id <Octra.raw.base.Peer peer_id>`, *optional*):
            N/A

        reply_to (:obj:`MessageReplyHeader date <Octra.raw.base.MessageReplyHeader date>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "action", "mentioned", "silent", "legacy", "from_id", "reply_to"]

    ID = 0x2b085862
    QUALNAME = "types.MessageService"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD out", action: "raw.base.MessageAction ttl_period", mentioned: "raw.base.true media_unread" = None, silent: "raw.base.true post" = None, legacy: "raw.base.true id" = None, from_id: "raw.base.Peer peer_id" = None, reply_to: "raw.base.MessageReplyHeader date" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD out
        self.action = action  # t.me/TheVenomXD MessageAction ttl_period
        self.mentioned = mentioned  # t.me/TheVenomXD flags.4?true media_unread
        self.silent = silent  # t.me/TheVenomXD flags.13?true post
        self.legacy = legacy  # t.me/TheVenomXD flags.19?true id
        self.from_id = from_id  # t.me/TheVenomXD flags.8?Peer peer_id
        self.reply_to = reply_to  # t.me/TheVenomXD flags.3?MessageReplyHeader date

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageService":
        
        flags = TLObject.read(b)
        
        mentioned = True if flags & (1 << 4) else False
        silent = True if flags & (1 << 13) else False
        legacy = True if flags & (1 << 19) else False
        from_id = TLObject.read(b) if flags & (1 << 8) else None
        
        reply_to = TLObject.read(b) if flags & (1 << 3) else None
        
        action = TLObject.read(b)
        
        return MessageService(flags=flags, action=action, mentioned=mentioned, silent=silent, legacy=legacy, from_id=from_id, reply_to=reply_to)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.from_id is not None:
            b.write(self.from_id.write())
        
        if self.reply_to is not None:
            b.write(self.reply_to.write())
        
        b.write(self.action.write())
        
        return b.getvalue()
