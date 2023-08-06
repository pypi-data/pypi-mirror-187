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


class EditGroupCallParticipant(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``A5273ABF``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD call <Octra.raw.base.# t.me/TheVenomXD call>`):
            N/A

        participant (:obj:`InputPeer muted <Octra.raw.base.InputPeer muted>`):
            N/A

        volume (:obj:`int raise_hand <Octra.raw.base.int raise_hand>`, *optional*):
            N/A

        video_stopped (:obj:`Bool video_paused <Octra.raw.base.Bool video_paused>`, *optional*):
            N/A

        presentation_paused (:obj:`Bool  <Octra.raw.base.Bool >`, *optional*):
            N/A

    Returns:
        :obj:`Updates <Octra.raw.base.Updates>`
    """

    __slots__: List[str] = ["flags", "participant", "volume", "video_stopped", "presentation_paused"]

    ID = 0xa5273abf
    QUALNAME = "functions.phone.EditGroupCallParticipant"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD call", participant: "raw.base.InputPeer muted", volume: "raw.base.int raise_hand" = None, video_stopped: "raw.base.Bool video_paused" = None, presentation_paused: "raw.base.Bool " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD call
        self.participant = participant  # t.me/TheVenomXD InputPeer muted
        self.volume = volume  # t.me/TheVenomXD flags.1?int raise_hand
        self.video_stopped = video_stopped  # t.me/TheVenomXD flags.3?Bool video_paused
        self.presentation_paused = presentation_paused  # t.me/TheVenomXD flags.5?Bool 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EditGroupCallParticipant":
        
        flags = TLObject.read(b)
        
        participant = TLObject.read(b)
        
        volume = Int.read(b) if flags & (1 << 1) else None
        video_stopped = Bool.read(b) if flags & (1 << 3) else None
        presentation_paused = Bool.read(b) if flags & (1 << 5) else None
        return EditGroupCallParticipant(flags=flags, participant=participant, volume=volume, video_stopped=video_stopped, presentation_paused=presentation_paused)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.participant.write())
        
        if self.volume is not None:
            b.write(Int(self.volume))
        
        if self.video_stopped is not None:
            b.write(Bool(self.video_stopped))
        
        if self.presentation_paused is not None:
            b.write(Bool(self.presentation_paused))
        
        return b.getvalue()
