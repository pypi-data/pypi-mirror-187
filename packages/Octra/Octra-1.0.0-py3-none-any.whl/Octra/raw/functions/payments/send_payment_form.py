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


class SendPaymentForm(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``2D03522F``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD form_id <Octra.raw.base.# t.me/TheVenomXD form_id>`):
            N/A

        invoice (:obj:`InputInvoice requested_info_id <Octra.raw.base.InputInvoice requested_info_id>`):
            N/A

        shipping_option_id (:obj:`string credentials <Octra.raw.base.string credentials>`, *optional*):
            N/A

        tip_amount (:obj:`long  <Octra.raw.base.long >`, *optional*):
            N/A

    Returns:
        :obj:`payments.PaymentResult <Octra.raw.base.payments.PaymentResult>`
    """

    __slots__: List[str] = ["flags", "invoice", "shipping_option_id", "tip_amount"]

    ID = 0x2d03522f
    QUALNAME = "functions.payments.SendPaymentForm"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD form_id", invoice: "raw.base.InputInvoice requested_info_id", shipping_option_id: "raw.base.string credentials" = None, tip_amount: "raw.base.long " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD form_id
        self.invoice = invoice  # t.me/TheVenomXD InputInvoice requested_info_id
        self.shipping_option_id = shipping_option_id  # t.me/TheVenomXD flags.1?string credentials
        self.tip_amount = tip_amount  # t.me/TheVenomXD flags.2?long 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendPaymentForm":
        
        flags = TLObject.read(b)
        
        invoice = TLObject.read(b)
        
        shipping_option_id = String.read(b) if flags & (1 << 1) else None
        tip_amount = Long.read(b) if flags & (1 << 2) else None
        return SendPaymentForm(flags=flags, invoice=invoice, shipping_option_id=shipping_option_id, tip_amount=tip_amount)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.invoice.write())
        
        if self.shipping_option_id is not None:
            b.write(String(self.shipping_option_id))
        
        if self.tip_amount is not None:
            b.write(Long(self.tip_amount))
        
        return b.getvalue()
