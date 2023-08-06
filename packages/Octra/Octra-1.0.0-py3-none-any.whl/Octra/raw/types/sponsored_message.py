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


class SponsoredMessage(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.SponsoredMessage`.

    Details:
        - Layer: ``151``
        - ID: ``3A836DF8``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD recommended <Octra.raw.base.# t.me/TheVenomXD recommended>`):
            N/A

        show_peer_photo (:obj:`true random_id <Octra.raw.base.true random_id>`, *optional*):
            N/A

        from_id (:obj:`Peer chat_invite <Octra.raw.base.Peer chat_invite>`, *optional*):
            N/A

        chat_invite_hash (:obj:`string channel_post <Octra.raw.base.string channel_post>`, *optional*):
            N/A

        start_param (:obj:`string message <Octra.raw.base.string message>`, *optional*):
            N/A

        entities (List of :obj:`MessageEntity> <Octra.raw.base.MessageEntity>>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "show_peer_photo", "from_id", "chat_invite_hash", "start_param", "entities"]

    ID = 0x3a836df8
    QUALNAME = "types.SponsoredMessage"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD recommended", show_peer_photo: "raw.base.true random_id" = None, from_id: "raw.base.Peer chat_invite" = None, chat_invite_hash: "raw.base.string channel_post" = None, start_param: "raw.base.string message" = None, entities: Optional[List["raw.base.MessageEntity>"]] = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD recommended
        self.show_peer_photo = show_peer_photo  # t.me/TheVenomXD flags.6?true random_id
        self.from_id = from_id  # t.me/TheVenomXD flags.3?Peer chat_invite
        self.chat_invite_hash = chat_invite_hash  # t.me/TheVenomXD flags.4?string channel_post
        self.start_param = start_param  # t.me/TheVenomXD flags.0?string message
        self.entities = entities  # t.me/TheVenomXD flags.1?Vector<MessageEntity> 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SponsoredMessage":
        
        flags = TLObject.read(b)
        
        show_peer_photo = True if flags & (1 << 6) else False
        from_id = TLObject.read(b) if flags & (1 << 3) else None
        
        chat_invite_hash = String.read(b) if flags & (1 << 4) else None
        start_param = String.read(b) if flags & (1 << 0) else None
        entities = TLObject.read(b) if flags & (1 << 1) else []
        
        return SponsoredMessage(flags=flags, show_peer_photo=show_peer_photo, from_id=from_id, chat_invite_hash=chat_invite_hash, start_param=start_param, entities=entities)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.from_id is not None:
            b.write(self.from_id.write())
        
        if self.chat_invite_hash is not None:
            b.write(String(self.chat_invite_hash))
        
        if self.start_param is not None:
            b.write(String(self.start_param))
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        return b.getvalue()
