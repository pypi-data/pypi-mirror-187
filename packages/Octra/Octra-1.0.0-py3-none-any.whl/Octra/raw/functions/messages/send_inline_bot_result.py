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


class SendInlineBotResult(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``D3FBDCCB``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD silent <Octra.raw.base.# t.me/TheVenomXD silent>`):
            N/A

        random_id (:obj:`long query_id <Octra.raw.base.long query_id>`):
            N/A

        id (:obj:`string schedule_date <Octra.raw.base.string schedule_date>`):
            N/A

        background (:obj:`true clear_draft <Octra.raw.base.true clear_draft>`, *optional*):
            N/A

        hide_via (:obj:`true peer <Octra.raw.base.true peer>`, *optional*):
            N/A

        reply_to_msg_id (:obj:`int top_msg_id <Octra.raw.base.int top_msg_id>`, *optional*):
            N/A

        send_as (:obj:`InputPeer  <Octra.raw.base.InputPeer >`, *optional*):
            N/A

    Returns:
        :obj:`Updates <Octra.raw.base.Updates>`
    """

    __slots__: List[str] = ["flags", "random_id", "id", "background", "hide_via", "reply_to_msg_id", "send_as"]

    ID = 0xd3fbdccb
    QUALNAME = "functions.messages.SendInlineBotResult"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD silent", random_id: "raw.base.long query_id", id: "raw.base.string schedule_date", background: "raw.base.true clear_draft" = None, hide_via: "raw.base.true peer" = None, reply_to_msg_id: "raw.base.int top_msg_id" = None, send_as: "raw.base.InputPeer " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD silent
        self.random_id = random_id  # t.me/TheVenomXD long query_id
        self.id = id  # t.me/TheVenomXD string schedule_date
        self.background = background  # t.me/TheVenomXD flags.6?true clear_draft
        self.hide_via = hide_via  # t.me/TheVenomXD flags.11?true peer
        self.reply_to_msg_id = reply_to_msg_id  # t.me/TheVenomXD flags.0?int top_msg_id
        self.send_as = send_as  # t.me/TheVenomXD flags.13?InputPeer 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendInlineBotResult":
        
        flags = TLObject.read(b)
        
        background = True if flags & (1 << 6) else False
        hide_via = True if flags & (1 << 11) else False
        reply_to_msg_id = Int.read(b) if flags & (1 << 0) else None
        random_id = TLObject.read(b)
        
        id = TLObject.read(b)
        
        send_as = TLObject.read(b) if flags & (1 << 13) else None
        
        return SendInlineBotResult(flags=flags, random_id=random_id, id=id, background=background, hide_via=hide_via, reply_to_msg_id=reply_to_msg_id, send_as=send_as)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.reply_to_msg_id is not None:
            b.write(Int(self.reply_to_msg_id))
        
        b.write(self.random_id.write())
        
        b.write(self.id.write())
        
        if self.send_as is not None:
            b.write(self.send_as.write())
        
        return b.getvalue()
