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


class CreateForumTopic(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``F40C0224``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD channel <Octra.raw.base.# t.me/TheVenomXD channel>`):
            N/A

        title (:obj:`string icon_color <Octra.raw.base.string icon_color>`):
            N/A

        icon_emoji_id (:obj:`long random_id <Octra.raw.base.long random_id>`, *optional*):
            N/A

        send_as (:obj:`InputPeer  <Octra.raw.base.InputPeer >`, *optional*):
            N/A

    Returns:
        :obj:`Updates <Octra.raw.base.Updates>`
    """

    __slots__: List[str] = ["flags", "title", "icon_emoji_id", "send_as"]

    ID = 0xf40c0224
    QUALNAME = "functions.channels.CreateForumTopic"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD channel", title: "raw.base.string icon_color", icon_emoji_id: "raw.base.long random_id" = None, send_as: "raw.base.InputPeer " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD channel
        self.title = title  # t.me/TheVenomXD string icon_color
        self.icon_emoji_id = icon_emoji_id  # t.me/TheVenomXD flags.3?long random_id
        self.send_as = send_as  # t.me/TheVenomXD flags.2?InputPeer 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CreateForumTopic":
        
        flags = TLObject.read(b)
        
        title = TLObject.read(b)
        
        icon_emoji_id = Long.read(b) if flags & (1 << 3) else None
        send_as = TLObject.read(b) if flags & (1 << 2) else None
        
        return CreateForumTopic(flags=flags, title=title, icon_emoji_id=icon_emoji_id, send_as=send_as)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.title.write())
        
        if self.icon_emoji_id is not None:
            b.write(Long(self.icon_emoji_id))
        
        if self.send_as is not None:
            b.write(self.send_as.write())
        
        return b.getvalue()
