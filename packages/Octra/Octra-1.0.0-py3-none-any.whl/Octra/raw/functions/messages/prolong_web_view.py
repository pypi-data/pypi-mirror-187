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


class ProlongWebView(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``7FF34309``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD silent <Octra.raw.base.# t.me/TheVenomXD silent>`):
            N/A

        peer (:obj:`InputPeer bot <Octra.raw.base.InputPeer bot>`):
            N/A

        query_id (:obj:`long reply_to_msg_id <Octra.raw.base.long reply_to_msg_id>`):
            N/A

        top_msg_id (:obj:`int send_as <Octra.raw.base.int send_as>`, *optional*):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["flags", "peer", "query_id", "top_msg_id"]

    ID = 0x7ff34309
    QUALNAME = "functions.messages.ProlongWebView"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD silent", peer: "raw.base.InputPeer bot", query_id: "raw.base.long reply_to_msg_id", top_msg_id: "raw.base.int send_as" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD silent
        self.peer = peer  # t.me/TheVenomXD InputPeer bot
        self.query_id = query_id  # t.me/TheVenomXD long reply_to_msg_id
        self.top_msg_id = top_msg_id  # t.me/TheVenomXD flags.9?int send_as

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ProlongWebView":
        
        flags = TLObject.read(b)
        
        peer = TLObject.read(b)
        
        query_id = TLObject.read(b)
        
        top_msg_id = Int.read(b) if flags & (1 << 9) else None
        return ProlongWebView(flags=flags, peer=peer, query_id=query_id, top_msg_id=top_msg_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.peer.write())
        
        b.write(self.query_id.write())
        
        if self.top_msg_id is not None:
            b.write(Int(self.top_msg_id))
        
        return b.getvalue()
