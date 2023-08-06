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


class ChatInvite(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.ChatInvite`.

    Details:
        - Layer: ``151``
        - ID: ``300C44C1``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD channel <Octra.raw.base.# t.me/TheVenomXD channel>`):
            N/A

        title (:obj:`string about <Octra.raw.base.string about>`):
            N/A

        photo (:obj:`Photo participants_count <Octra.raw.base.Photo participants_count>`):
            N/A

        broadcast (:obj:`true public <Octra.raw.base.true public>`, *optional*):
            N/A

        megagroup (:obj:`true request_needed <Octra.raw.base.true request_needed>`, *optional*):
            N/A

        participants (List of :obj:`User> <Octra.raw.base.User>>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            messages.CheckChatInvite
    """

    __slots__: List[str] = ["flags", "title", "photo", "broadcast", "megagroup", "participants"]

    ID = 0x300c44c1
    QUALNAME = "types.ChatInvite"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD channel", title: "raw.base.string about", photo: "raw.base.Photo participants_count", broadcast: "raw.base.true public" = None, megagroup: "raw.base.true request_needed" = None, participants: Optional[List["raw.base.User>"]] = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD channel
        self.title = title  # t.me/TheVenomXD string about
        self.photo = photo  # t.me/TheVenomXD Photo participants_count
        self.broadcast = broadcast  # t.me/TheVenomXD flags.1?true public
        self.megagroup = megagroup  # t.me/TheVenomXD flags.3?true request_needed
        self.participants = participants  # t.me/TheVenomXD flags.4?Vector<User> 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChatInvite":
        
        flags = TLObject.read(b)
        
        broadcast = True if flags & (1 << 1) else False
        megagroup = True if flags & (1 << 3) else False
        title = TLObject.read(b)
        
        photo = TLObject.read(b)
        
        participants = TLObject.read(b) if flags & (1 << 4) else []
        
        return ChatInvite(flags=flags, title=title, photo=photo, broadcast=broadcast, megagroup=megagroup, participants=participants)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.title.write())
        
        b.write(self.photo.write())
        
        if self.participants is not None:
            b.write(Vector(self.participants))
        
        return b.getvalue()
