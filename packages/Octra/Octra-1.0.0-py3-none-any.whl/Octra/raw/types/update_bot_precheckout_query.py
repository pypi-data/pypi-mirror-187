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


class UpdateBotPrecheckoutQuery(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Update`.

    Details:
        - Layer: ``151``
        - ID: ``8CAA9A96``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD query_id <Octra.raw.base.# t.me/TheVenomXD query_id>`):
            N/A

        octra_user_id (:obj:`long payload <Octra.raw.base.long payload>`):
            N/A

        currency (:obj:`string total_amount <Octra.raw.base.string total_amount>`):
            N/A

        info (:obj:`PaymentRequestedInfo shipping_option_id <Octra.raw.base.PaymentRequestedInfo shipping_option_id>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "octra_user_id", "currency", "info"]

    ID = 0x8caa9a96
    QUALNAME = "types.UpdateBotPrecheckoutQuery"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD query_id", octra_user_id: "raw.base.long payload", currency: "raw.base.string total_amount", info: "raw.base.PaymentRequestedInfo shipping_option_id" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD query_id
        self.octra_user_id = octra_user_id  # t.me/TheVenomXD long payload
        self.currency = currency  # t.me/TheVenomXD string total_amount
        self.info = info  # t.me/TheVenomXD flags.0?PaymentRequestedInfo shipping_option_id

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateBotPrecheckoutQuery":
        
        flags = TLObject.read(b)
        
        octra_user_id = TLObject.read(b)
        
        info = TLObject.read(b) if flags & (1 << 0) else None
        
        currency = TLObject.read(b)
        
        return UpdateBotPrecheckoutQuery(flags=flags, octra_user_id=octra_user_id, currency=currency, info=info)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.octra_user_id.write())
        
        if self.info is not None:
            b.write(self.info.write())
        
        b.write(self.currency.write())
        
        return b.getvalue()
