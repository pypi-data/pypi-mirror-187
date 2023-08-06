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


class ChannelDifferenceTooLong(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.updates.ChannelDifference`.

    Details:
        - Layer: ``151``
        - ID: ``A4BCC6FE``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD final <Octra.raw.base.# t.me/TheVenomXD final>`):
            N/A

        messages (List of :obj:`Message> chat <Octra.raw.base.Message> chat>`):
            N/A

        users (List of :obj:`User> <Octra.raw.base.User>>`):
            N/A

        timeout (:obj:`int dialog <Octra.raw.base.int dialog>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            updates.GetChannelDifference
    """

    __slots__: List[str] = ["flags", "messages", "users", "timeout"]

    ID = 0xa4bcc6fe
    QUALNAME = "types.updates.ChannelDifferenceTooLong"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD final", messages: List["raw.base.Message> chat"], users: List["raw.base.User>"], timeout: "raw.base.int dialog" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD final
        self.messages = messages  # t.me/TheVenomXD Vector<Message> chats
        self.users = users  # t.me/TheVenomXD Vector<User> 
        self.timeout = timeout  # t.me/TheVenomXD flags.1?int dialog

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelDifferenceTooLong":
        
        flags = TLObject.read(b)
        
        timeout = Int.read(b) if flags & (1 << 1) else None
        messages = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return ChannelDifferenceTooLong(flags=flags, messages=messages, users=users, timeout=timeout)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.timeout is not None:
            b.write(Int(self.timeout))
        
        b.write(Vector(self.messages))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
