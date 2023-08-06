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


class EditForumTopic(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``F4DFA185``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD channel <Octra.raw.base.# t.me/TheVenomXD channel>`):
            N/A

        topic_id (:obj:`int title <Octra.raw.base.int title>`):
            N/A

        icon_emoji_id (:obj:`long closed <Octra.raw.base.long closed>`, *optional*):
            N/A

        hidden (:obj:`Bool  <Octra.raw.base.Bool >`, *optional*):
            N/A

    Returns:
        :obj:`Updates <Octra.raw.base.Updates>`
    """

    __slots__: List[str] = ["flags", "topic_id", "icon_emoji_id", "hidden"]

    ID = 0xf4dfa185
    QUALNAME = "functions.channels.EditForumTopic"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD channel", topic_id: "raw.base.int title", icon_emoji_id: "raw.base.long closed" = None, hidden: "raw.base.Bool " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD channel
        self.topic_id = topic_id  # t.me/TheVenomXD int title
        self.icon_emoji_id = icon_emoji_id  # t.me/TheVenomXD flags.1?long closed
        self.hidden = hidden  # t.me/TheVenomXD flags.3?Bool 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EditForumTopic":
        
        flags = TLObject.read(b)
        
        topic_id = TLObject.read(b)
        
        icon_emoji_id = Long.read(b) if flags & (1 << 1) else None
        hidden = Bool.read(b) if flags & (1 << 3) else None
        return EditForumTopic(flags=flags, topic_id=topic_id, icon_emoji_id=icon_emoji_id, hidden=hidden)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.topic_id.write())
        
        if self.icon_emoji_id is not None:
            b.write(Long(self.icon_emoji_id))
        
        if self.hidden is not None:
            b.write(Bool(self.hidden))
        
        return b.getvalue()
