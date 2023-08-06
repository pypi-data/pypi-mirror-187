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


class MessageMediaInvoice(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.MessageMedia`.

    Details:
        - Layer: ``151``
        - ID: ``F6A548D3``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD shipping_address_requested <Octra.raw.base.# t.me/TheVenomXD shipping_address_requested>`):
            N/A

        description (:obj:`string photo <Octra.raw.base.string photo>`):
            N/A

        total_amount (:obj:`long start_param <Octra.raw.base.long start_param>`):
            N/A

        test (:obj:`true title <Octra.raw.base.true title>`, *optional*):
            N/A

        receipt_msg_id (:obj:`int currency <Octra.raw.base.int currency>`, *optional*):
            N/A

        extended_media (:obj:`MessageExtendedMedia  <Octra.raw.base.MessageExtendedMedia >`, *optional*):
            N/A

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetWebPagePreview
            messages.UploadMedia
            messages.UploadImportedMedia
    """

    __slots__: List[str] = ["flags", "description", "total_amount", "test", "receipt_msg_id", "extended_media"]

    ID = 0xf6a548d3
    QUALNAME = "types.MessageMediaInvoice"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD shipping_address_requested", description: "raw.base.string photo", total_amount: "raw.base.long start_param", test: "raw.base.true title" = None, receipt_msg_id: "raw.base.int currency" = None, extended_media: "raw.base.MessageExtendedMedia " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD shipping_address_requested
        self.description = description  # t.me/TheVenomXD string photo
        self.total_amount = total_amount  # t.me/TheVenomXD long start_param
        self.test = test  # t.me/TheVenomXD flags.3?true title
        self.receipt_msg_id = receipt_msg_id  # t.me/TheVenomXD flags.2?int currency
        self.extended_media = extended_media  # t.me/TheVenomXD flags.4?MessageExtendedMedia 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageMediaInvoice":
        
        flags = TLObject.read(b)
        
        test = True if flags & (1 << 3) else False
        description = TLObject.read(b)
        
        receipt_msg_id = Int.read(b) if flags & (1 << 2) else None
        total_amount = TLObject.read(b)
        
        extended_media = TLObject.read(b) if flags & (1 << 4) else None
        
        return MessageMediaInvoice(flags=flags, description=description, total_amount=total_amount, test=test, receipt_msg_id=receipt_msg_id, extended_media=extended_media)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.description.write())
        
        if self.receipt_msg_id is not None:
            b.write(Int(self.receipt_msg_id))
        
        b.write(self.total_amount.write())
        
        if self.extended_media is not None:
            b.write(self.extended_media.write())
        
        return b.getvalue()
