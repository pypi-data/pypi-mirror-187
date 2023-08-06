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


class InputMediaInvoice(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.InputMedia`.

    Details:
        - Layer: ``151``
        - ID: ``8EB5A6D5``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD title <Octra.raw.base.# t.me/TheVenomXD title>`):
            N/A

        description (:obj:`string photo <Octra.raw.base.string photo>`):
            N/A

        invoice (:obj:`Invoice payload <Octra.raw.base.Invoice payload>`):
            N/A

        provider (:obj:`string provider_data <Octra.raw.base.string provider_data>`):
            N/A

        start_param (:obj:`string extended_media <Octra.raw.base.string extended_media>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "description", "invoice", "provider", "start_param"]

    ID = 0x8eb5a6d5
    QUALNAME = "types.InputMediaInvoice"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD title", description: "raw.base.string photo", invoice: "raw.base.Invoice payload", provider: "raw.base.string provider_data", start_param: "raw.base.string extended_media" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD title
        self.description = description  # t.me/TheVenomXD string photo
        self.invoice = invoice  # t.me/TheVenomXD Invoice payload
        self.provider = provider  # t.me/TheVenomXD string provider_data
        self.start_param = start_param  # t.me/TheVenomXD flags.1?string extended_media

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputMediaInvoice":
        
        flags = TLObject.read(b)
        
        description = TLObject.read(b)
        
        invoice = TLObject.read(b)
        
        provider = TLObject.read(b)
        
        start_param = String.read(b) if flags & (1 << 1) else None
        return InputMediaInvoice(flags=flags, description=description, invoice=invoice, provider=provider, start_param=start_param)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.description.write())
        
        b.write(self.invoice.write())
        
        b.write(self.provider.write())
        
        if self.start_param is not None:
            b.write(String(self.start_param))
        
        return b.getvalue()
