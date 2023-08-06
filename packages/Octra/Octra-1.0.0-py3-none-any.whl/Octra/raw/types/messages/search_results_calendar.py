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


class SearchResultsCalendar(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.messages.SearchResultsCalendar`.

    Details:
        - Layer: ``151``
        - ID: ``147EE23C``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD inexact <Octra.raw.base.# t.me/TheVenomXD inexact>`):
            N/A

        count (:obj:`int min_date <Octra.raw.base.int min_date>`):
            N/A

        min_msg_id (:obj:`int offset_id_offset <Octra.raw.base.int offset_id_offset>`):
            N/A

        periods (List of :obj:`SearchResultsCalendarPeriod> message <Octra.raw.base.SearchResultsCalendarPeriod> message>`):
            N/A

        chats (List of :obj:`Chat> user <Octra.raw.base.Chat> user>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetSearchResultsCalendar
    """

    __slots__: List[str] = ["flags", "count", "min_msg_id", "periods", "chats"]

    ID = 0x147ee23c
    QUALNAME = "types.messages.SearchResultsCalendar"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD inexact", count: "raw.base.int min_date", min_msg_id: "raw.base.int offset_id_offset", periods: List["raw.base.SearchResultsCalendarPeriod> message"], chats: List["raw.base.Chat> user"]) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD inexact
        self.count = count  # t.me/TheVenomXD int min_date
        self.min_msg_id = min_msg_id  # t.me/TheVenomXD int offset_id_offset
        self.periods = periods  # t.me/TheVenomXD Vector<SearchResultsCalendarPeriod> messages
        self.chats = chats  # t.me/TheVenomXD Vector<Chat> users

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SearchResultsCalendar":
        
        flags = TLObject.read(b)
        
        count = TLObject.read(b)
        
        min_msg_id = TLObject.read(b)
        
        periods = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        return SearchResultsCalendar(flags=flags, count=count, min_msg_id=min_msg_id, periods=periods, chats=chats)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.count.write())
        
        b.write(self.min_msg_id.write())
        
        b.write(Vector(self.periods))
        
        b.write(Vector(self.chats))
        
        return b.getvalue()
