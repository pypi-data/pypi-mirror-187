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


class PremiumSubscriptionOption(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.PremiumSubscriptionOption`.

    Details:
        - Layer: ``151``
        - ID: ``B6F11EBE``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD current <Octra.raw.base.# t.me/TheVenomXD current>`):
            N/A

        currency (:obj:`string amount <Octra.raw.base.string amount>`):
            N/A

        bot_url (:obj:`string store_product <Octra.raw.base.string store_product>`):
            N/A

        can_purchase_upgrade (:obj:`true months <Octra.raw.base.true months>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "currency", "bot_url", "can_purchase_upgrade"]

    ID = 0xb6f11ebe
    QUALNAME = "types.PremiumSubscriptionOption"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD current", currency: "raw.base.string amount", bot_url: "raw.base.string store_product", can_purchase_upgrade: "raw.base.true months" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD current
        self.currency = currency  # t.me/TheVenomXD string amount
        self.bot_url = bot_url  # t.me/TheVenomXD string store_product
        self.can_purchase_upgrade = can_purchase_upgrade  # t.me/TheVenomXD flags.2?true months

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PremiumSubscriptionOption":
        
        flags = TLObject.read(b)
        
        can_purchase_upgrade = True if flags & (1 << 2) else False
        currency = TLObject.read(b)
        
        bot_url = TLObject.read(b)
        
        return PremiumSubscriptionOption(flags=flags, currency=currency, bot_url=bot_url, can_purchase_upgrade=can_purchase_upgrade)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.currency.write())
        
        b.write(self.bot_url.write())
        
        return b.getvalue()
