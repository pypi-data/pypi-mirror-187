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


class PaymentReceipt(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.payments.PaymentReceipt`.

    Details:
        - Layer: ``151``
        - ID: ``70C4FE03``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD date <Octra.raw.base.# t.me/TheVenomXD date>`):
            N/A

        bot_id (:obj:`long provider_id <Octra.raw.base.long provider_id>`):
            N/A

        title (:obj:`string description <Octra.raw.base.string description>`):
            N/A

        total_amount (:obj:`long credentials_title <Octra.raw.base.long credentials_title>`):
            N/A

        users (List of :obj:`User> <Octra.raw.base.User>>`):
            N/A

        photo (:obj:`WebDocument invoice <Octra.raw.base.WebDocument invoice>`, *optional*):
            N/A

        info (:obj:`PaymentRequestedInfo shipping <Octra.raw.base.PaymentRequestedInfo shipping>`, *optional*):
            N/A

        tip_amount (:obj:`long currency <Octra.raw.base.long currency>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            payments.GetPaymentReceipt
    """

    __slots__: List[str] = ["flags", "bot_id", "title", "total_amount", "users", "photo", "info", "tip_amount"]

    ID = 0x70c4fe03
    QUALNAME = "types.payments.PaymentReceipt"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD date", bot_id: "raw.base.long provider_id", title: "raw.base.string description", total_amount: "raw.base.long credentials_title", users: List["raw.base.User>"], photo: "raw.base.WebDocument invoice" = None, info: "raw.base.PaymentRequestedInfo shipping" = None, tip_amount: "raw.base.long currency" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD date
        self.bot_id = bot_id  # t.me/TheVenomXD long provider_id
        self.title = title  # t.me/TheVenomXD string description
        self.total_amount = total_amount  # t.me/TheVenomXD long credentials_title
        self.users = users  # t.me/TheVenomXD Vector<User> 
        self.photo = photo  # t.me/TheVenomXD flags.2?WebDocument invoice
        self.info = info  # t.me/TheVenomXD flags.0?PaymentRequestedInfo shipping
        self.tip_amount = tip_amount  # t.me/TheVenomXD flags.3?long currency

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PaymentReceipt":
        
        flags = TLObject.read(b)
        
        bot_id = TLObject.read(b)
        
        title = TLObject.read(b)
        
        photo = TLObject.read(b) if flags & (1 << 2) else None
        
        info = TLObject.read(b) if flags & (1 << 0) else None
        
        tip_amount = Long.read(b) if flags & (1 << 3) else None
        total_amount = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return PaymentReceipt(flags=flags, bot_id=bot_id, title=title, total_amount=total_amount, users=users, photo=photo, info=info, tip_amount=tip_amount)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.bot_id.write())
        
        b.write(self.title.write())
        
        if self.photo is not None:
            b.write(self.photo.write())
        
        if self.info is not None:
            b.write(self.info.write())
        
        if self.tip_amount is not None:
            b.write(Long(self.tip_amount))
        
        b.write(self.total_amount.write())
        
        b.write(Vector(self.users))
        
        return b.getvalue()
