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


class SendMultiMedia(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``B6F11A1C``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD silent <Octra.raw.base.# t.me/TheVenomXD silent>`):
            N/A

        peer (:obj:`InputPeer reply_to_msg_id <Octra.raw.base.InputPeer reply_to_msg_id>`):
            N/A

        background (:obj:`true clear_draft <Octra.raw.base.true clear_draft>`, *optional*):
            N/A

        noforwards (:obj:`true update_stickersets_order <Octra.raw.base.true update_stickersets_order>`, *optional*):
            N/A

        top_msg_id (:obj:`int multi_media <Octra.raw.base.int multi_media>`, *optional*):
            N/A

        schedule_date (:obj:`int send_as <Octra.raw.base.int send_as>`, *optional*):
            N/A

    Returns:
        :obj:`Updates <Octra.raw.base.Updates>`
    """

    __slots__: List[str] = ["flags", "peer", "background", "noforwards", "top_msg_id", "schedule_date"]

    ID = 0xb6f11a1c
    QUALNAME = "functions.messages.SendMultiMedia"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD silent", peer: "raw.base.InputPeer reply_to_msg_id", background: "raw.base.true clear_draft" = None, noforwards: "raw.base.true update_stickersets_order" = None, top_msg_id: "raw.base.int multi_media" = None, schedule_date: "raw.base.int send_as" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD silent
        self.peer = peer  # t.me/TheVenomXD InputPeer reply_to_msg_id
        self.background = background  # t.me/TheVenomXD flags.6?true clear_draft
        self.noforwards = noforwards  # t.me/TheVenomXD flags.14?true update_stickersets_order
        self.top_msg_id = top_msg_id  # t.me/TheVenomXD flags.9?int multi_media
        self.schedule_date = schedule_date  # t.me/TheVenomXD flags.10?int send_as

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendMultiMedia":
        
        flags = TLObject.read(b)
        
        background = True if flags & (1 << 6) else False
        noforwards = True if flags & (1 << 14) else False
        peer = TLObject.read(b)
        
        top_msg_id = Int.read(b) if flags & (1 << 9) else None
        schedule_date = Int.read(b) if flags & (1 << 10) else None
        return SendMultiMedia(flags=flags, peer=peer, background=background, noforwards=noforwards, top_msg_id=top_msg_id, schedule_date=schedule_date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.peer.write())
        
        if self.top_msg_id is not None:
            b.write(Int(self.top_msg_id))
        
        if self.schedule_date is not None:
            b.write(Int(self.schedule_date))
        
        return b.getvalue()
