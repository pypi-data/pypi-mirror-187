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


class SendMedia(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``7547C966``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD silent <Octra.raw.base.# t.me/TheVenomXD silent>`):
            N/A

        peer (:obj:`InputPeer reply_to_msg_id <Octra.raw.base.InputPeer reply_to_msg_id>`):
            N/A

        message (:obj:`string random_id <Octra.raw.base.string random_id>`):
            N/A

        background (:obj:`true clear_draft <Octra.raw.base.true clear_draft>`, *optional*):
            N/A

        noforwards (:obj:`true update_stickersets_order <Octra.raw.base.true update_stickersets_order>`, *optional*):
            N/A

        top_msg_id (:obj:`int media <Octra.raw.base.int media>`, *optional*):
            N/A

        reply_markup (:obj:`ReplyMarkup entities <Octra.raw.base.ReplyMarkup entities>`, *optional*):
            N/A

        schedule_date (:obj:`int send_as <Octra.raw.base.int send_as>`, *optional*):
            N/A

    Returns:
        :obj:`Updates <Octra.raw.base.Updates>`
    """

    __slots__: List[str] = ["flags", "peer", "message", "background", "noforwards", "top_msg_id", "reply_markup", "schedule_date"]

    ID = 0x7547c966
    QUALNAME = "functions.messages.SendMedia"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD silent", peer: "raw.base.InputPeer reply_to_msg_id", message: "raw.base.string random_id", background: "raw.base.true clear_draft" = None, noforwards: "raw.base.true update_stickersets_order" = None, top_msg_id: "raw.base.int media" = None, reply_markup: "raw.base.ReplyMarkup entities" = None, schedule_date: "raw.base.int send_as" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD silent
        self.peer = peer  # t.me/TheVenomXD InputPeer reply_to_msg_id
        self.message = message  # t.me/TheVenomXD string random_id
        self.background = background  # t.me/TheVenomXD flags.6?true clear_draft
        self.noforwards = noforwards  # t.me/TheVenomXD flags.14?true update_stickersets_order
        self.top_msg_id = top_msg_id  # t.me/TheVenomXD flags.9?int media
        self.reply_markup = reply_markup  # t.me/TheVenomXD flags.2?ReplyMarkup entities
        self.schedule_date = schedule_date  # t.me/TheVenomXD flags.10?int send_as

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendMedia":
        
        flags = TLObject.read(b)
        
        background = True if flags & (1 << 6) else False
        noforwards = True if flags & (1 << 14) else False
        peer = TLObject.read(b)
        
        top_msg_id = Int.read(b) if flags & (1 << 9) else None
        message = TLObject.read(b)
        
        reply_markup = TLObject.read(b) if flags & (1 << 2) else None
        
        schedule_date = Int.read(b) if flags & (1 << 10) else None
        return SendMedia(flags=flags, peer=peer, message=message, background=background, noforwards=noforwards, top_msg_id=top_msg_id, reply_markup=reply_markup, schedule_date=schedule_date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.peer.write())
        
        if self.top_msg_id is not None:
            b.write(Int(self.top_msg_id))
        
        b.write(self.message.write())
        
        if self.reply_markup is not None:
            b.write(self.reply_markup.write())
        
        if self.schedule_date is not None:
            b.write(Int(self.schedule_date))
        
        return b.getvalue()
