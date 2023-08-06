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


class ChannelAdminLogEventsFlow(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.ChannelAdminLogEventsFlow`.

    Details:
        - Layer: ``151``
        - ID: ``EA107AE4``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD join <Octra.raw.base.# t.me/TheVenomXD join>`):
            N/A

        leave (:obj:`true invite <Octra.raw.base.true invite>`, *optional*):
            N/A

        ban (:obj:`true unban <Octra.raw.base.true unban>`, *optional*):
            N/A

        kick (:obj:`true unkick <Octra.raw.base.true unkick>`, *optional*):
            N/A

        promote (:obj:`true demote <Octra.raw.base.true demote>`, *optional*):
            N/A

        info (:obj:`true settings <Octra.raw.base.true settings>`, *optional*):
            N/A

        pinned (:obj:`true edit <Octra.raw.base.true edit>`, *optional*):
            N/A

        delete (:obj:`true group_call <Octra.raw.base.true group_call>`, *optional*):
            N/A

        invites (:obj:`true send <Octra.raw.base.true send>`, *optional*):
            N/A

        forums (:obj:`true  <Octra.raw.base.true >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "leave", "ban", "kick", "promote", "info", "pinned", "delete", "invites", "forums"]

    ID = 0xea107ae4
    QUALNAME = "types.ChannelAdminLogEventsFlow"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD join", leave: "raw.base.true invite" = None, ban: "raw.base.true unban" = None, kick: "raw.base.true unkick" = None, promote: "raw.base.true demote" = None, info: "raw.base.true settings" = None, pinned: "raw.base.true edit" = None, delete: "raw.base.true group_call" = None, invites: "raw.base.true send" = None, forums: "raw.base.true " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD join
        self.leave = leave  # t.me/TheVenomXD flags.1?true invite
        self.ban = ban  # t.me/TheVenomXD flags.3?true unban
        self.kick = kick  # t.me/TheVenomXD flags.5?true unkick
        self.promote = promote  # t.me/TheVenomXD flags.7?true demote
        self.info = info  # t.me/TheVenomXD flags.9?true settings
        self.pinned = pinned  # t.me/TheVenomXD flags.11?true edit
        self.delete = delete  # t.me/TheVenomXD flags.13?true group_call
        self.invites = invites  # t.me/TheVenomXD flags.15?true send
        self.forums = forums  # t.me/TheVenomXD flags.17?true 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelAdminLogEventsFlow":
        
        flags = TLObject.read(b)
        
        leave = True if flags & (1 << 1) else False
        ban = True if flags & (1 << 3) else False
        kick = True if flags & (1 << 5) else False
        promote = True if flags & (1 << 7) else False
        info = True if flags & (1 << 9) else False
        pinned = True if flags & (1 << 11) else False
        delete = True if flags & (1 << 13) else False
        invites = True if flags & (1 << 15) else False
        forums = True if flags & (1 << 17) else False
        return ChannelAdminLogEventsFlow(flags=flags, leave=leave, ban=ban, kick=kick, promote=promote, info=info, pinned=pinned, delete=delete, invites=invites, forums=forums)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        return b.getvalue()
