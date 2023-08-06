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


class InputBotInlineMessageMediaInvoice(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.InputBotInlineMessage`.

    Details:
        - Layer: ``151``
        - ID: ``D7E78225``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD title <Octra.raw.base.# t.me/TheVenomXD title>`):
            N/A

        description (:obj:`string photo <Octra.raw.base.string photo>`):
            N/A

        invoice (:obj:`Invoice payload <Octra.raw.base.Invoice payload>`):
            N/A

        provider (:obj:`string provider_data <Octra.raw.base.string provider_data>`):
            N/A

        reply_markup (:obj:`ReplyMarkup  <Octra.raw.base.ReplyMarkup >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "description", "invoice", "provider", "reply_markup"]

    ID = 0xd7e78225
    QUALNAME = "types.InputBotInlineMessageMediaInvoice"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD title", description: "raw.base.string photo", invoice: "raw.base.Invoice payload", provider: "raw.base.string provider_data", reply_markup: "raw.base.ReplyMarkup " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD title
        self.description = description  # t.me/TheVenomXD string photo
        self.invoice = invoice  # t.me/TheVenomXD Invoice payload
        self.provider = provider  # t.me/TheVenomXD string provider_data
        self.reply_markup = reply_markup  # t.me/TheVenomXD flags.2?ReplyMarkup 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputBotInlineMessageMediaInvoice":
        
        flags = TLObject.read(b)
        
        description = TLObject.read(b)
        
        invoice = TLObject.read(b)
        
        provider = TLObject.read(b)
        
        reply_markup = TLObject.read(b) if flags & (1 << 2) else None
        
        return InputBotInlineMessageMediaInvoice(flags=flags, description=description, invoice=invoice, provider=provider, reply_markup=reply_markup)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.description.write())
        
        b.write(self.invoice.write())
        
        b.write(self.provider.write())
        
        if self.reply_markup is not None:
            b.write(self.reply_markup.write())
        
        return b.getvalue()
