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


class BotCallbackAnswer(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.messages.BotCallbackAnswer`.

    Details:
        - Layer: ``151``
        - ID: ``36585EA4``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD alert <Octra.raw.base.# t.me/TheVenomXD alert>`):
            N/A

        cache_time (:obj:`int  <Octra.raw.base.int >`):
            N/A

        has_url (:obj:`true native_ui <Octra.raw.base.true native_ui>`, *optional*):
            N/A

        message (:obj:`string url <Octra.raw.base.string url>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetBotCallbackAnswer
    """

    __slots__: List[str] = ["flags", "cache_time", "has_url", "message"]

    ID = 0x36585ea4
    QUALNAME = "types.messages.BotCallbackAnswer"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD alert", cache_time: "raw.base.int ", has_url: "raw.base.true native_ui" = None, message: "raw.base.string url" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD alert
        self.cache_time = cache_time  # t.me/TheVenomXD int 
        self.has_url = has_url  # t.me/TheVenomXD flags.3?true native_ui
        self.message = message  # t.me/TheVenomXD flags.0?string url

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BotCallbackAnswer":
        
        flags = TLObject.read(b)
        
        has_url = True if flags & (1 << 3) else False
        message = String.read(b) if flags & (1 << 0) else None
        cache_time = TLObject.read(b)
        
        return BotCallbackAnswer(flags=flags, cache_time=cache_time, has_url=has_url, message=message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.message is not None:
            b.write(String(self.message))
        
        b.write(self.cache_time.write())
        
        return b.getvalue()
