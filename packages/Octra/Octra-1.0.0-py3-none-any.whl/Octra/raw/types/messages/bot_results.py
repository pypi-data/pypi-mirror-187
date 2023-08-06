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


class BotResults(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.messages.BotResults`.

    Details:
        - Layer: ``151``
        - ID: ``947CA848``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD gallery <Octra.raw.base.# t.me/TheVenomXD gallery>`):
            N/A

        query_id (:obj:`long next_offset <Octra.raw.base.long next_offset>`):
            N/A

        cache_time (:obj:`int users <Octra.raw.base.int users>`):
            N/A

        switch_pm (:obj:`InlineBotSwitchPM results <Octra.raw.base.InlineBotSwitchPM results>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetInlineBotResults
    """

    __slots__: List[str] = ["flags", "query_id", "cache_time", "switch_pm"]

    ID = 0x947ca848
    QUALNAME = "types.messages.BotResults"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD gallery", query_id: "raw.base.long next_offset", cache_time: "raw.base.int users", switch_pm: "raw.base.InlineBotSwitchPM results" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD gallery
        self.query_id = query_id  # t.me/TheVenomXD long next_offset
        self.cache_time = cache_time  # t.me/TheVenomXD int users
        self.switch_pm = switch_pm  # t.me/TheVenomXD flags.2?InlineBotSwitchPM results

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BotResults":
        
        flags = TLObject.read(b)
        
        query_id = TLObject.read(b)
        
        switch_pm = TLObject.read(b) if flags & (1 << 2) else None
        
        cache_time = TLObject.read(b)
        
        return BotResults(flags=flags, query_id=query_id, cache_time=cache_time, switch_pm=switch_pm)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.query_id.write())
        
        if self.switch_pm is not None:
            b.write(self.switch_pm.write())
        
        b.write(self.cache_time.write())
        
        return b.getvalue()
