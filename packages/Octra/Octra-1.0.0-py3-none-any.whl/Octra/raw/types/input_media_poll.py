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


class InputMediaPoll(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.InputMedia`.

    Details:
        - Layer: ``151``
        - ID: ``F94E5F1``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD poll <Octra.raw.base.# t.me/TheVenomXD poll>`):
            N/A

        correct_answers (List of :obj:`bytes> solutio <Octra.raw.base.bytes> solutio>`, *optional*):
            N/A

        solution_entities (List of :obj:`MessageEntity> <Octra.raw.base.MessageEntity>>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "correct_answers", "solution_entities"]

    ID = 0xf94e5f1
    QUALNAME = "types.InputMediaPoll"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD poll", correct_answers: Optional[List["raw.base.bytes> solutio"]] = None, solution_entities: Optional[List["raw.base.MessageEntity>"]] = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD poll
        self.correct_answers = correct_answers  # t.me/TheVenomXD flags.0?Vector<bytes> solution
        self.solution_entities = solution_entities  # t.me/TheVenomXD flags.1?Vector<MessageEntity> 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputMediaPoll":
        
        flags = TLObject.read(b)
        
        correct_answers = TLObject.read(b) if flags & (1 << 0) else []
        
        solution_entities = TLObject.read(b) if flags & (1 << 1) else []
        
        return InputMediaPoll(flags=flags, correct_answers=correct_answers, solution_entities=solution_entities)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.correct_answers is not None:
            b.write(Vector(self.correct_answers))
        
        if self.solution_entities is not None:
            b.write(Vector(self.solution_entities))
        
        return b.getvalue()
