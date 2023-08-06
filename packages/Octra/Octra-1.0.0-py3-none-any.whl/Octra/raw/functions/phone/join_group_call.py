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


class JoinGroupCall(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``B132FF7B``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD muted <Octra.raw.base.# t.me/TheVenomXD muted>`):
            N/A

        join_as (:obj:`InputPeer invite_hash <Octra.raw.base.InputPeer invite_hash>`):
            N/A

        params (:obj:`DataJSON  <Octra.raw.base.DataJSON >`):
            N/A

        video_stopped (:obj:`true call <Octra.raw.base.true call>`, *optional*):
            N/A

    Returns:
        :obj:`Updates <Octra.raw.base.Updates>`
    """

    __slots__: List[str] = ["flags", "join_as", "params", "video_stopped"]

    ID = 0xb132ff7b
    QUALNAME = "functions.phone.JoinGroupCall"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD muted", join_as: "raw.base.InputPeer invite_hash", params: "raw.base.DataJSON ", video_stopped: "raw.base.true call" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD muted
        self.join_as = join_as  # t.me/TheVenomXD InputPeer invite_hash
        self.params = params  # t.me/TheVenomXD DataJSON 
        self.video_stopped = video_stopped  # t.me/TheVenomXD flags.2?true call

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "JoinGroupCall":
        
        flags = TLObject.read(b)
        
        video_stopped = True if flags & (1 << 2) else False
        join_as = TLObject.read(b)
        
        params = TLObject.read(b)
        
        return JoinGroupCall(flags=flags, join_as=join_as, params=params, video_stopped=video_stopped)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.join_as.write())
        
        b.write(self.params.write())
        
        return b.getvalue()
