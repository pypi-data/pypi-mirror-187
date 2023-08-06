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


class ForwardMessages(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``C661BBC4``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD silent <Octra.raw.base.# t.me/TheVenomXD silent>`):
            N/A

        id (List of :obj:`int> random_i <Octra.raw.base.int> random_i>`):
            N/A

        to_peer (:obj:`InputPeer top_msg_id <Octra.raw.base.InputPeer top_msg_id>`):
            N/A

        background (:obj:`true with_my_score <Octra.raw.base.true with_my_score>`, *optional*):
            N/A

        drop_author (:obj:`true drop_media_captions <Octra.raw.base.true drop_media_captions>`, *optional*):
            N/A

        noforwards (:obj:`true from_peer <Octra.raw.base.true from_peer>`, *optional*):
            N/A

        schedule_date (:obj:`int send_as <Octra.raw.base.int send_as>`, *optional*):
            N/A

    Returns:
        :obj:`Updates <Octra.raw.base.Updates>`
    """

    __slots__: List[str] = ["flags", "id", "to_peer", "background", "drop_author", "noforwards", "schedule_date"]

    ID = 0xc661bbc4
    QUALNAME = "functions.messages.ForwardMessages"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD silent", id: List["raw.base.int> random_i"], to_peer: "raw.base.InputPeer top_msg_id", background: "raw.base.true with_my_score" = None, drop_author: "raw.base.true drop_media_captions" = None, noforwards: "raw.base.true from_peer" = None, schedule_date: "raw.base.int send_as" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD silent
        self.id = id  # t.me/TheVenomXD Vector<int> random_id
        self.to_peer = to_peer  # t.me/TheVenomXD InputPeer top_msg_id
        self.background = background  # t.me/TheVenomXD flags.6?true with_my_score
        self.drop_author = drop_author  # t.me/TheVenomXD flags.11?true drop_media_captions
        self.noforwards = noforwards  # t.me/TheVenomXD flags.14?true from_peer
        self.schedule_date = schedule_date  # t.me/TheVenomXD flags.10?int send_as

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ForwardMessages":
        
        flags = TLObject.read(b)
        
        background = True if flags & (1 << 6) else False
        drop_author = True if flags & (1 << 11) else False
        noforwards = True if flags & (1 << 14) else False
        id = TLObject.read(b)
        
        to_peer = TLObject.read(b)
        
        schedule_date = Int.read(b) if flags & (1 << 10) else None
        return ForwardMessages(flags=flags, id=id, to_peer=to_peer, background=background, drop_author=drop_author, noforwards=noforwards, schedule_date=schedule_date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(Vector(self.id))
        
        b.write(self.to_peer.write())
        
        if self.schedule_date is not None:
            b.write(Int(self.schedule_date))
        
        return b.getvalue()
