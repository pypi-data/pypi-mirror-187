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


class BotInlineMessageMediaInvoice(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.BotInlineMessage`.

    Details:
        - Layer: ``151``
        - ID: ``354A9B09``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD shipping_address_requested <Octra.raw.base.# t.me/TheVenomXD shipping_address_requested>`):
            N/A

        description (:obj:`string photo <Octra.raw.base.string photo>`):
            N/A

        currency (:obj:`string total_amount <Octra.raw.base.string total_amount>`):
            N/A

        test (:obj:`true title <Octra.raw.base.true title>`, *optional*):
            N/A

        reply_markup (:obj:`ReplyMarkup  <Octra.raw.base.ReplyMarkup >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "description", "currency", "test", "reply_markup"]

    ID = 0x354a9b09
    QUALNAME = "types.BotInlineMessageMediaInvoice"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD shipping_address_requested", description: "raw.base.string photo", currency: "raw.base.string total_amount", test: "raw.base.true title" = None, reply_markup: "raw.base.ReplyMarkup " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD shipping_address_requested
        self.description = description  # t.me/TheVenomXD string photo
        self.currency = currency  # t.me/TheVenomXD string total_amount
        self.test = test  # t.me/TheVenomXD flags.3?true title
        self.reply_markup = reply_markup  # t.me/TheVenomXD flags.2?ReplyMarkup 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BotInlineMessageMediaInvoice":
        
        flags = TLObject.read(b)
        
        test = True if flags & (1 << 3) else False
        description = TLObject.read(b)
        
        currency = TLObject.read(b)
        
        reply_markup = TLObject.read(b) if flags & (1 << 2) else None
        
        return BotInlineMessageMediaInvoice(flags=flags, description=description, currency=currency, test=test, reply_markup=reply_markup)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.description.write())
        
        b.write(self.currency.write())
        
        if self.reply_markup is not None:
            b.write(self.reply_markup.write())
        
        return b.getvalue()
