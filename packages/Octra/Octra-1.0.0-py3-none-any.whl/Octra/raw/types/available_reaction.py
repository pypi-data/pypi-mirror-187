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


class AvailableReaction(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.AvailableReaction`.

    Details:
        - Layer: ``151``
        - ID: ``C077EC01``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD inactive <Octra.raw.base.# t.me/TheVenomXD inactive>`):
            N/A

        title (:obj:`string static_icon <Octra.raw.base.string static_icon>`):
            N/A

        appear_animation (:obj:`Document select_animation <Octra.raw.base.Document select_animation>`):
            N/A

        activate_animation (:obj:`Document effect_animation <Octra.raw.base.Document effect_animation>`):
            N/A

        premium (:obj:`true reaction <Octra.raw.base.true reaction>`, *optional*):
            N/A

        around_animation (:obj:`Document center_icon <Octra.raw.base.Document center_icon>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "title", "appear_animation", "activate_animation", "premium", "around_animation"]

    ID = 0xc077ec01
    QUALNAME = "types.AvailableReaction"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD inactive", title: "raw.base.string static_icon", appear_animation: "raw.base.Document select_animation", activate_animation: "raw.base.Document effect_animation", premium: "raw.base.true reaction" = None, around_animation: "raw.base.Document center_icon" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD inactive
        self.title = title  # t.me/TheVenomXD string static_icon
        self.appear_animation = appear_animation  # t.me/TheVenomXD Document select_animation
        self.activate_animation = activate_animation  # t.me/TheVenomXD Document effect_animation
        self.premium = premium  # t.me/TheVenomXD flags.2?true reaction
        self.around_animation = around_animation  # t.me/TheVenomXD flags.1?Document center_icon

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AvailableReaction":
        
        flags = TLObject.read(b)
        
        premium = True if flags & (1 << 2) else False
        title = TLObject.read(b)
        
        appear_animation = TLObject.read(b)
        
        activate_animation = TLObject.read(b)
        
        around_animation = TLObject.read(b) if flags & (1 << 1) else None
        
        return AvailableReaction(flags=flags, title=title, appear_animation=appear_animation, activate_animation=activate_animation, premium=premium, around_animation=around_animation)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.title.write())
        
        b.write(self.appear_animation.write())
        
        b.write(self.activate_animation.write())
        
        if self.around_animation is not None:
            b.write(self.around_animation.write())
        
        return b.getvalue()
