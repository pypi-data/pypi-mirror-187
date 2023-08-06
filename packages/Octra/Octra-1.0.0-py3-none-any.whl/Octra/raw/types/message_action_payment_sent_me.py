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


class MessageActionPaymentSentMe(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.MessageAction`.

    Details:
        - Layer: ``151``
        - ID: ``8F31B327``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD recurring_init <Octra.raw.base.# t.me/TheVenomXD recurring_init>`):
            N/A

        total_amount (:obj:`long payload <Octra.raw.base.long payload>`):
            N/A

        charge (:obj:`PaymentCharge  <Octra.raw.base.PaymentCharge >`):
            N/A

        recurring_used (:obj:`true currency <Octra.raw.base.true currency>`, *optional*):
            N/A

        info (:obj:`PaymentRequestedInfo shipping_option_id <Octra.raw.base.PaymentRequestedInfo shipping_option_id>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "total_amount", "charge", "recurring_used", "info"]

    ID = 0x8f31b327
    QUALNAME = "types.MessageActionPaymentSentMe"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD recurring_init", total_amount: "raw.base.long payload", charge: "raw.base.PaymentCharge ", recurring_used: "raw.base.true currency" = None, info: "raw.base.PaymentRequestedInfo shipping_option_id" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD recurring_init
        self.total_amount = total_amount  # t.me/TheVenomXD long payload
        self.charge = charge  # t.me/TheVenomXD PaymentCharge 
        self.recurring_used = recurring_used  # t.me/TheVenomXD flags.3?true currency
        self.info = info  # t.me/TheVenomXD flags.0?PaymentRequestedInfo shipping_option_id

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionPaymentSentMe":
        
        flags = TLObject.read(b)
        
        recurring_used = True if flags & (1 << 3) else False
        total_amount = TLObject.read(b)
        
        info = TLObject.read(b) if flags & (1 << 0) else None
        
        charge = TLObject.read(b)
        
        return MessageActionPaymentSentMe(flags=flags, total_amount=total_amount, charge=charge, recurring_used=recurring_used, info=info)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.total_amount.write())
        
        if self.info is not None:
            b.write(self.info.write())
        
        b.write(self.charge.write())
        
        return b.getvalue()
