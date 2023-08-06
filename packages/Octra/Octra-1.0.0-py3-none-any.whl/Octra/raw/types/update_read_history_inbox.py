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


class UpdateReadHistoryInbox(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Update`.

    Details:
        - Layer: ``151``
        - ID: ``9C974FDF``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD folder_id <Octra.raw.base.# t.me/TheVenomXD folder_id>`):
            N/A

        peer (:obj:`Peer max_id <Octra.raw.base.Peer max_id>`):
            N/A

        still_unread_count (:obj:`int pts <Octra.raw.base.int pts>`):
            N/A

        pts_count (:obj:`int  <Octra.raw.base.int >`):
            N/A

    """

    __slots__: List[str] = ["flags", "peer", "still_unread_count", "pts_count"]

    ID = 0x9c974fdf
    QUALNAME = "types.UpdateReadHistoryInbox"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD folder_id", peer: "raw.base.Peer max_id", still_unread_count: "raw.base.int pts", pts_count: "raw.base.int ") -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD folder_id
        self.peer = peer  # t.me/TheVenomXD Peer max_id
        self.still_unread_count = still_unread_count  # t.me/TheVenomXD int pts
        self.pts_count = pts_count  # t.me/TheVenomXD int 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateReadHistoryInbox":
        
        flags = TLObject.read(b)
        
        peer = TLObject.read(b)
        
        still_unread_count = TLObject.read(b)
        
        pts_count = TLObject.read(b)
        
        return UpdateReadHistoryInbox(flags=flags, peer=peer, still_unread_count=still_unread_count, pts_count=pts_count)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.peer.write())
        
        b.write(self.still_unread_count.write())
        
        b.write(self.pts_count.write())
        
        return b.getvalue()
