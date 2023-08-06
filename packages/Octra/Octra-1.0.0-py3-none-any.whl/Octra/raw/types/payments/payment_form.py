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


class PaymentForm(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.payments.PaymentForm`.

    Details:
        - Layer: ``151``
        - ID: ``A0058751``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD can_save_credentials <Octra.raw.base.# t.me/TheVenomXD can_save_credentials>`):
            N/A

        bot_id (:obj:`long title <Octra.raw.base.long title>`):
            N/A

        description (:obj:`string photo <Octra.raw.base.string photo>`):
            N/A

        invoice (:obj:`Invoice provider_id <Octra.raw.base.Invoice provider_id>`):
            N/A

        url (:obj:`string native_provider <Octra.raw.base.string native_provider>`):
            N/A

        users (List of :obj:`User> <Octra.raw.base.User>>`):
            N/A

        password_missing (:obj:`true form_id <Octra.raw.base.true form_id>`, *optional*):
            N/A

        native_params (:obj:`DataJSON additional_methods <Octra.raw.base.DataJSON additional_methods>`, *optional*):
            N/A

        saved_info (:obj:`PaymentRequestedInfo saved_credentials <Octra.raw.base.PaymentRequestedInfo saved_credentials>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            payments.GetPaymentForm
    """

    __slots__: List[str] = ["flags", "bot_id", "description", "invoice", "url", "users", "password_missing", "native_params", "saved_info"]

    ID = 0xa0058751
    QUALNAME = "types.payments.PaymentForm"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD can_save_credentials", bot_id: "raw.base.long title", description: "raw.base.string photo", invoice: "raw.base.Invoice provider_id", url: "raw.base.string native_provider", users: List["raw.base.User>"], password_missing: "raw.base.true form_id" = None, native_params: "raw.base.DataJSON additional_methods" = None, saved_info: "raw.base.PaymentRequestedInfo saved_credentials" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD can_save_credentials
        self.bot_id = bot_id  # t.me/TheVenomXD long title
        self.description = description  # t.me/TheVenomXD string photo
        self.invoice = invoice  # t.me/TheVenomXD Invoice provider_id
        self.url = url  # t.me/TheVenomXD string native_provider
        self.users = users  # t.me/TheVenomXD Vector<User> 
        self.password_missing = password_missing  # t.me/TheVenomXD flags.3?true form_id
        self.native_params = native_params  # t.me/TheVenomXD flags.4?DataJSON additional_methods
        self.saved_info = saved_info  # t.me/TheVenomXD flags.0?PaymentRequestedInfo saved_credentials

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PaymentForm":
        
        flags = TLObject.read(b)
        
        password_missing = True if flags & (1 << 3) else False
        bot_id = TLObject.read(b)
        
        description = TLObject.read(b)
        
        invoice = TLObject.read(b)
        
        url = TLObject.read(b)
        
        native_params = TLObject.read(b) if flags & (1 << 4) else None
        
        saved_info = TLObject.read(b) if flags & (1 << 0) else None
        
        users = TLObject.read(b)
        
        return PaymentForm(flags=flags, bot_id=bot_id, description=description, invoice=invoice, url=url, users=users, password_missing=password_missing, native_params=native_params, saved_info=saved_info)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.bot_id.write())
        
        b.write(self.description.write())
        
        b.write(self.invoice.write())
        
        b.write(self.url.write())
        
        if self.native_params is not None:
            b.write(self.native_params.write())
        
        if self.saved_info is not None:
            b.write(self.saved_info.write())
        
        b.write(Vector(self.users))
        
        return b.getvalue()
