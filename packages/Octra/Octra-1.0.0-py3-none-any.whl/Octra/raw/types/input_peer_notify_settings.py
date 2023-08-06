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


class InputPeerNotifySettings(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.InputPeerNotifySettings`.

    Details:
        - Layer: ``151``
        - ID: ``DF1F002B``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD show_previews <Octra.raw.base.# t.me/TheVenomXD show_previews>`):
            N/A

        silent (:obj:`Bool mute_until <Octra.raw.base.Bool mute_until>`, *optional*):
            N/A

        sound (:obj:`NotificationSound  <Octra.raw.base.NotificationSound >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "silent", "sound"]

    ID = 0xdf1f002b
    QUALNAME = "types.InputPeerNotifySettings"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD show_previews", silent: "raw.base.Bool mute_until" = None, sound: "raw.base.NotificationSound " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD show_previews
        self.silent = silent  # t.me/TheVenomXD flags.1?Bool mute_until
        self.sound = sound  # t.me/TheVenomXD flags.3?NotificationSound 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPeerNotifySettings":
        
        flags = TLObject.read(b)
        
        silent = Bool.read(b) if flags & (1 << 1) else None
        sound = TLObject.read(b) if flags & (1 << 3) else None
        
        return InputPeerNotifySettings(flags=flags, silent=silent, sound=sound)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.silent is not None:
            b.write(Bool(self.silent))
        
        if self.sound is not None:
            b.write(self.sound.write())
        
        return b.getvalue()
