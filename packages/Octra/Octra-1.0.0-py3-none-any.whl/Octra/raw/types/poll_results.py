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


class PollResults(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.PollResults`.

    Details:
        - Layer: ``151``
        - ID: ``DCB82EA3``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD min <Octra.raw.base.# t.me/TheVenomXD min>`):
            N/A

        results (List of :obj:`PollAnswerVoters> total_voter <Octra.raw.base.PollAnswerVoters> total_voter>`, *optional*):
            N/A

        recent_voters (List of :obj:`long> solutio <Octra.raw.base.long> solutio>`, *optional*):
            N/A

        solution_entities (List of :obj:`MessageEntity> <Octra.raw.base.MessageEntity>>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "results", "recent_voters", "solution_entities"]

    ID = 0xdcb82ea3
    QUALNAME = "types.PollResults"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD min", results: Optional[List["raw.base.PollAnswerVoters> total_voter"]] = None, recent_voters: Optional[List["raw.base.long> solutio"]] = None, solution_entities: Optional[List["raw.base.MessageEntity>"]] = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD min
        self.results = results  # t.me/TheVenomXD flags.1?Vector<PollAnswerVoters> total_voters
        self.recent_voters = recent_voters  # t.me/TheVenomXD flags.3?Vector<long> solution
        self.solution_entities = solution_entities  # t.me/TheVenomXD flags.4?Vector<MessageEntity> 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PollResults":
        
        flags = TLObject.read(b)
        
        results = TLObject.read(b) if flags & (1 << 1) else []
        
        recent_voters = TLObject.read(b) if flags & (1 << 3) else []
        
        solution_entities = TLObject.read(b) if flags & (1 << 4) else []
        
        return PollResults(flags=flags, results=results, recent_voters=recent_voters, solution_entities=solution_entities)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.results is not None:
            b.write(Vector(self.results))
        
        if self.recent_voters is not None:
            b.write(Vector(self.recent_voters))
        
        if self.solution_entities is not None:
            b.write(Vector(self.solution_entities))
        
        return b.getvalue()
