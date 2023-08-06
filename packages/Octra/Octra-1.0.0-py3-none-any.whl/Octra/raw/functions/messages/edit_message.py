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


class EditMessage(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``48F71778``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD no_webpage <Octra.raw.base.# t.me/TheVenomXD no_webpage>`):
            N/A

        peer (:obj:`InputPeer id <Octra.raw.base.InputPeer id>`):
            N/A

        message (:obj:`string media <Octra.raw.base.string media>`, *optional*):
            N/A

        reply_markup (:obj:`ReplyMarkup entities <Octra.raw.base.ReplyMarkup entities>`, *optional*):
            N/A

        schedule_date (:obj:`int  <Octra.raw.base.int >`, *optional*):
            N/A

    Returns:
        :obj:`Updates <Octra.raw.base.Updates>`
    """

    __slots__: List[str] = ["flags", "peer", "message", "reply_markup", "schedule_date"]

    ID = 0x48f71778
    QUALNAME = "functions.messages.EditMessage"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD no_webpage", peer: "raw.base.InputPeer id", message: "raw.base.string media" = None, reply_markup: "raw.base.ReplyMarkup entities" = None, schedule_date: "raw.base.int " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD no_webpage
        self.peer = peer  # t.me/TheVenomXD InputPeer id
        self.message = message  # t.me/TheVenomXD flags.11?string media
        self.reply_markup = reply_markup  # t.me/TheVenomXD flags.2?ReplyMarkup entities
        self.schedule_date = schedule_date  # t.me/TheVenomXD flags.15?int 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EditMessage":
        
        flags = TLObject.read(b)
        
        peer = TLObject.read(b)
        
        message = String.read(b) if flags & (1 << 11) else None
        reply_markup = TLObject.read(b) if flags & (1 << 2) else None
        
        schedule_date = Int.read(b) if flags & (1 << 15) else None
        return EditMessage(flags=flags, peer=peer, message=message, reply_markup=reply_markup, schedule_date=schedule_date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.peer.write())
        
        if self.message is not None:
            b.write(String(self.message))
        
        if self.reply_markup is not None:
            b.write(self.reply_markup.write())
        
        if self.schedule_date is not None:
            b.write(Int(self.schedule_date))
        
        return b.getvalue()
