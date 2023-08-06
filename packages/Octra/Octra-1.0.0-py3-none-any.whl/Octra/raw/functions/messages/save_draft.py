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


class SaveDraft(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``B4331E3F``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD no_webpage <Octra.raw.base.# t.me/TheVenomXD no_webpage>`):
            N/A

        peer (:obj:`InputPeer message <Octra.raw.base.InputPeer message>`):
            N/A

        reply_to_msg_id (:obj:`int top_msg_id <Octra.raw.base.int top_msg_id>`, *optional*):
            N/A

        entities (List of :obj:`MessageEntity> <Octra.raw.base.MessageEntity>>`, *optional*):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["flags", "peer", "reply_to_msg_id", "entities"]

    ID = 0xb4331e3f
    QUALNAME = "functions.messages.SaveDraft"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD no_webpage", peer: "raw.base.InputPeer message", reply_to_msg_id: "raw.base.int top_msg_id" = None, entities: Optional[List["raw.base.MessageEntity>"]] = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD no_webpage
        self.peer = peer  # t.me/TheVenomXD InputPeer message
        self.reply_to_msg_id = reply_to_msg_id  # t.me/TheVenomXD flags.0?int top_msg_id
        self.entities = entities  # t.me/TheVenomXD flags.3?Vector<MessageEntity> 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SaveDraft":
        
        flags = TLObject.read(b)
        
        reply_to_msg_id = Int.read(b) if flags & (1 << 0) else None
        peer = TLObject.read(b)
        
        entities = TLObject.read(b) if flags & (1 << 3) else []
        
        return SaveDraft(flags=flags, peer=peer, reply_to_msg_id=reply_to_msg_id, entities=entities)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.reply_to_msg_id is not None:
            b.write(Int(self.reply_to_msg_id))
        
        b.write(self.peer.write())
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        return b.getvalue()
