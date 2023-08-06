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


class AttachMenuBot(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.AttachMenuBot`.

    Details:
        - Layer: ``151``
        - ID: ``C8AA2CD2``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD inactive <Octra.raw.base.# t.me/TheVenomXD inactive>`):
            N/A

        bot_id (:obj:`long short_name <Octra.raw.base.long short_name>`):
            N/A

        peer_types (List of :obj:`AttachMenuPeerType> icon <Octra.raw.base.AttachMenuPeerType> icon>`):
            N/A

        has_settings (:obj:`true request_write_access <Octra.raw.base.true request_write_access>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "bot_id", "peer_types", "has_settings"]

    ID = 0xc8aa2cd2
    QUALNAME = "types.AttachMenuBot"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD inactive", bot_id: "raw.base.long short_name", peer_types: List["raw.base.AttachMenuPeerType> icon"], has_settings: "raw.base.true request_write_access" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD inactive
        self.bot_id = bot_id  # t.me/TheVenomXD long short_name
        self.peer_types = peer_types  # t.me/TheVenomXD Vector<AttachMenuPeerType> icons
        self.has_settings = has_settings  # t.me/TheVenomXD flags.1?true request_write_access

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AttachMenuBot":
        
        flags = TLObject.read(b)
        
        has_settings = True if flags & (1 << 1) else False
        bot_id = TLObject.read(b)
        
        peer_types = TLObject.read(b)
        
        return AttachMenuBot(flags=flags, bot_id=bot_id, peer_types=peer_types, has_settings=has_settings)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.bot_id.write())
        
        b.write(Vector(self.peer_types))
        
        return b.getvalue()
