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


class BotInlineMessageMediaVenue(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.BotInlineMessage`.

    Details:
        - Layer: ``151``
        - ID: ``8A86659C``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD geo <Octra.raw.base.# t.me/TheVenomXD geo>`):
            N/A

        title (:obj:`string address <Octra.raw.base.string address>`):
            N/A

        provider (:obj:`string venue_id <Octra.raw.base.string venue_id>`):
            N/A

        venue_type (:obj:`string reply_markup <Octra.raw.base.string reply_markup>`):
            N/A

    """

    __slots__: List[str] = ["flags", "title", "provider", "venue_type"]

    ID = 0x8a86659c
    QUALNAME = "types.BotInlineMessageMediaVenue"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD geo", title: "raw.base.string address", provider: "raw.base.string venue_id", venue_type: "raw.base.string reply_markup") -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD geo
        self.title = title  # t.me/TheVenomXD string address
        self.provider = provider  # t.me/TheVenomXD string venue_id
        self.venue_type = venue_type  # t.me/TheVenomXD string reply_markup

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BotInlineMessageMediaVenue":
        
        flags = TLObject.read(b)
        
        title = TLObject.read(b)
        
        provider = TLObject.read(b)
        
        venue_type = TLObject.read(b)
        
        return BotInlineMessageMediaVenue(flags=flags, title=title, provider=provider, venue_type=venue_type)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.title.write())
        
        b.write(self.provider.write())
        
        b.write(self.venue_type.write())
        
        return b.getvalue()
