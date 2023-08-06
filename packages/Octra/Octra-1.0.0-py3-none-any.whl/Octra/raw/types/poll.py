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


class Poll(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Poll`.

    Details:
        - Layer: ``151``
        - ID: ``86E18161``

    Parameters:
        id (:obj:`long flags <Octra.raw.base.long flags>`):
            N/A

        question (:obj:`string answers <Octra.raw.base.string answers>`):
            N/A

        closed (:obj:`true public_voters <Octra.raw.base.true public_voters>`, *optional*):
            N/A

        multiple_choice (:obj:`true quiz <Octra.raw.base.true quiz>`, *optional*):
            N/A

        close_period (:obj:`int close_date <Octra.raw.base.int close_date>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["id", "question", "closed", "multiple_choice", "close_period"]

    ID = 0x86e18161
    QUALNAME = "types.Poll"

    def __init__(self, *, id: "raw.base.long flags", question: "raw.base.string answers", closed: "raw.base.true public_voters" = None, multiple_choice: "raw.base.true quiz" = None, close_period: "raw.base.int close_date" = None) -> None:
        self.id = id  # t.me/TheVenomXD long flags
        self.question = question  # t.me/TheVenomXD string answers
        self.closed = closed  # t.me/TheVenomXD flags.0?true public_voters
        self.multiple_choice = multiple_choice  # t.me/TheVenomXD flags.2?true quiz
        self.close_period = close_period  # t.me/TheVenomXD flags.4?int close_date

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Poll":
        
        id = TLObject.read(b)
        
        closed = True if flags & (1 << 0) else False
        multiple_choice = True if flags & (1 << 2) else False
        question = TLObject.read(b)
        
        close_period = Int.read(b) if flags & (1 << 4) else None
        return Poll(id=id, question=question, closed=closed, multiple_choice=multiple_choice, close_period=close_period)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.id.write())
        
        b.write(self.question.write())
        
        if self.close_period is not None:
            b.write(Int(self.close_period))
        
        return b.getvalue()
