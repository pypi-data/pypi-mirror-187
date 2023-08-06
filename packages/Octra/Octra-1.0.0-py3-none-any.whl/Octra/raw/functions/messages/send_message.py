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


class SendMessage(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``1CC20387``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD no_webpage <Octra.raw.base.# t.me/TheVenomXD no_webpage>`):
            N/A

        message (:obj:`string random_id <Octra.raw.base.string random_id>`):
            N/A

        silent (:obj:`true background <Octra.raw.base.true background>`, *optional*):
            N/A

        clear_draft (:obj:`true noforwards <Octra.raw.base.true noforwards>`, *optional*):
            N/A

        update_stickersets_order (:obj:`true peer <Octra.raw.base.true peer>`, *optional*):
            N/A

        reply_to_msg_id (:obj:`int top_msg_id <Octra.raw.base.int top_msg_id>`, *optional*):
            N/A

        reply_markup (:obj:`ReplyMarkup entities <Octra.raw.base.ReplyMarkup entities>`, *optional*):
            N/A

        schedule_date (:obj:`int send_as <Octra.raw.base.int send_as>`, *optional*):
            N/A

    Returns:
        :obj:`Updates <Octra.raw.base.Updates>`
    """

    __slots__: List[str] = ["flags", "message", "silent", "clear_draft", "update_stickersets_order", "reply_to_msg_id", "reply_markup", "schedule_date"]

    ID = 0x1cc20387
    QUALNAME = "functions.messages.SendMessage"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD no_webpage", message: "raw.base.string random_id", silent: "raw.base.true background" = None, clear_draft: "raw.base.true noforwards" = None, update_stickersets_order: "raw.base.true peer" = None, reply_to_msg_id: "raw.base.int top_msg_id" = None, reply_markup: "raw.base.ReplyMarkup entities" = None, schedule_date: "raw.base.int send_as" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD no_webpage
        self.message = message  # t.me/TheVenomXD string random_id
        self.silent = silent  # t.me/TheVenomXD flags.5?true background
        self.clear_draft = clear_draft  # t.me/TheVenomXD flags.7?true noforwards
        self.update_stickersets_order = update_stickersets_order  # t.me/TheVenomXD flags.15?true peer
        self.reply_to_msg_id = reply_to_msg_id  # t.me/TheVenomXD flags.0?int top_msg_id
        self.reply_markup = reply_markup  # t.me/TheVenomXD flags.2?ReplyMarkup entities
        self.schedule_date = schedule_date  # t.me/TheVenomXD flags.10?int send_as

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendMessage":
        
        flags = TLObject.read(b)
        
        silent = True if flags & (1 << 5) else False
        clear_draft = True if flags & (1 << 7) else False
        update_stickersets_order = True if flags & (1 << 15) else False
        reply_to_msg_id = Int.read(b) if flags & (1 << 0) else None
        message = TLObject.read(b)
        
        reply_markup = TLObject.read(b) if flags & (1 << 2) else None
        
        schedule_date = Int.read(b) if flags & (1 << 10) else None
        return SendMessage(flags=flags, message=message, silent=silent, clear_draft=clear_draft, update_stickersets_order=update_stickersets_order, reply_to_msg_id=reply_to_msg_id, reply_markup=reply_markup, schedule_date=schedule_date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.reply_to_msg_id is not None:
            b.write(Int(self.reply_to_msg_id))
        
        b.write(self.message.write())
        
        if self.reply_markup is not None:
            b.write(self.reply_markup.write())
        
        if self.schedule_date is not None:
            b.write(Int(self.schedule_date))
        
        return b.getvalue()
