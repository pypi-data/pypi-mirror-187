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


class GroupCallParticipant(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.GroupCallParticipant`.

    Details:
        - Layer: ``151``
        - ID: ``EBA636FE``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD muted <Octra.raw.base.# t.me/TheVenomXD muted>`):
            N/A

        date (:obj:`int active_date <Octra.raw.base.int active_date>`):
            N/A

        source (:obj:`int volume <Octra.raw.base.int volume>`):
            N/A

        left (:obj:`true can_self_unmute <Octra.raw.base.true can_self_unmute>`, *optional*):
            N/A

        just_joined (:obj:`true versioned <Octra.raw.base.true versioned>`, *optional*):
            N/A

        min (:obj:`true muted_by_you <Octra.raw.base.true muted_by_you>`, *optional*):
            N/A

        volume_by_admin (:obj:`true self <Octra.raw.base.true self>`, *optional*):
            N/A

        video_joined (:obj:`true peer <Octra.raw.base.true peer>`, *optional*):
            N/A

        about (:obj:`string raise_hand_rating <Octra.raw.base.string raise_hand_rating>`, *optional*):
            N/A

        video (:obj:`GroupCallParticipantVideo presentation <Octra.raw.base.GroupCallParticipantVideo presentation>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "date", "source", "left", "just_joined", "min", "volume_by_admin", "video_joined", "about", "video"]

    ID = 0xeba636fe
    QUALNAME = "types.GroupCallParticipant"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD muted", date: "raw.base.int active_date", source: "raw.base.int volume", left: "raw.base.true can_self_unmute" = None, just_joined: "raw.base.true versioned" = None, min: "raw.base.true muted_by_you" = None, volume_by_admin: "raw.base.true self" = None, video_joined: "raw.base.true peer" = None, about: "raw.base.string raise_hand_rating" = None, video: "raw.base.GroupCallParticipantVideo presentation" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD muted
        self.date = date  # t.me/TheVenomXD int active_date
        self.source = source  # t.me/TheVenomXD int volume
        self.left = left  # t.me/TheVenomXD flags.1?true can_self_unmute
        self.just_joined = just_joined  # t.me/TheVenomXD flags.4?true versioned
        self.min = min  # t.me/TheVenomXD flags.8?true muted_by_you
        self.volume_by_admin = volume_by_admin  # t.me/TheVenomXD flags.10?true self
        self.video_joined = video_joined  # t.me/TheVenomXD flags.15?true peer
        self.about = about  # t.me/TheVenomXD flags.11?string raise_hand_rating
        self.video = video  # t.me/TheVenomXD flags.6?GroupCallParticipantVideo presentation

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GroupCallParticipant":
        
        flags = TLObject.read(b)
        
        left = True if flags & (1 << 1) else False
        just_joined = True if flags & (1 << 4) else False
        min = True if flags & (1 << 8) else False
        volume_by_admin = True if flags & (1 << 10) else False
        video_joined = True if flags & (1 << 15) else False
        date = TLObject.read(b)
        
        source = TLObject.read(b)
        
        about = String.read(b) if flags & (1 << 11) else None
        video = TLObject.read(b) if flags & (1 << 6) else None
        
        return GroupCallParticipant(flags=flags, date=date, source=source, left=left, just_joined=just_joined, min=min, volume_by_admin=volume_by_admin, video_joined=video_joined, about=about, video=video)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.date.write())
        
        b.write(self.source.write())
        
        if self.about is not None:
            b.write(String(self.about))
        
        if self.video is not None:
            b.write(self.video.write())
        
        return b.getvalue()
