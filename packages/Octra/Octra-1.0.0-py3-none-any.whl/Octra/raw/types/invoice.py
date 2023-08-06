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


class Invoice(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Invoice`.

    Details:
        - Layer: ``151``
        - ID: ``3E85A91B``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD test <Octra.raw.base.# t.me/TheVenomXD test>`):
            N/A

        currency (:obj:`string prices <Octra.raw.base.string prices>`):
            N/A

        name_requested (:obj:`true phone_requested <Octra.raw.base.true phone_requested>`, *optional*):
            N/A

        email_requested (:obj:`true shipping_address_requested <Octra.raw.base.true shipping_address_requested>`, *optional*):
            N/A

        flexible (:obj:`true phone_to_provider <Octra.raw.base.true phone_to_provider>`, *optional*):
            N/A

        email_to_provider (:obj:`true recurring <Octra.raw.base.true recurring>`, *optional*):
            N/A

        max_tip_amount (:obj:`long suggested_tip_amounts <Octra.raw.base.long suggested_tip_amounts>`, *optional*):
            N/A

        recurring_terms_url (:obj:`string  <Octra.raw.base.string >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "currency", "name_requested", "email_requested", "flexible", "email_to_provider", "max_tip_amount", "recurring_terms_url"]

    ID = 0x3e85a91b
    QUALNAME = "types.Invoice"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD test", currency: "raw.base.string prices", name_requested: "raw.base.true phone_requested" = None, email_requested: "raw.base.true shipping_address_requested" = None, flexible: "raw.base.true phone_to_provider" = None, email_to_provider: "raw.base.true recurring" = None, max_tip_amount: "raw.base.long suggested_tip_amounts" = None, recurring_terms_url: "raw.base.string " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD test
        self.currency = currency  # t.me/TheVenomXD string prices
        self.name_requested = name_requested  # t.me/TheVenomXD flags.1?true phone_requested
        self.email_requested = email_requested  # t.me/TheVenomXD flags.3?true shipping_address_requested
        self.flexible = flexible  # t.me/TheVenomXD flags.5?true phone_to_provider
        self.email_to_provider = email_to_provider  # t.me/TheVenomXD flags.7?true recurring
        self.max_tip_amount = max_tip_amount  # t.me/TheVenomXD flags.8?long suggested_tip_amounts
        self.recurring_terms_url = recurring_terms_url  # t.me/TheVenomXD flags.9?string 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Invoice":
        
        flags = TLObject.read(b)
        
        name_requested = True if flags & (1 << 1) else False
        email_requested = True if flags & (1 << 3) else False
        flexible = True if flags & (1 << 5) else False
        email_to_provider = True if flags & (1 << 7) else False
        currency = TLObject.read(b)
        
        max_tip_amount = Long.read(b) if flags & (1 << 8) else None
        recurring_terms_url = String.read(b) if flags & (1 << 9) else None
        return Invoice(flags=flags, currency=currency, name_requested=name_requested, email_requested=email_requested, flexible=flexible, email_to_provider=email_to_provider, max_tip_amount=max_tip_amount, recurring_terms_url=recurring_terms_url)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.currency.write())
        
        if self.max_tip_amount is not None:
            b.write(Long(self.max_tip_amount))
        
        if self.recurring_terms_url is not None:
            b.write(String(self.recurring_terms_url))
        
        return b.getvalue()
