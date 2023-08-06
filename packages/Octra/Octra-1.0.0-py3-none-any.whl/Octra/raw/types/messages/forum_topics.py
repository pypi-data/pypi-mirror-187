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


class ForumTopics(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.messages.ForumTopics`.

    Details:
        - Layer: ``151``
        - ID: ``367617D3``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD order_by_create_date <Octra.raw.base.# t.me/TheVenomXD order_by_create_date>`):
            N/A

        count (:obj:`int topics <Octra.raw.base.int topics>`):
            N/A

        messages (List of :obj:`Message> chat <Octra.raw.base.Message> chat>`):
            N/A

        users (List of :obj:`User> pt <Octra.raw.base.User> pt>`):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            channels.GetForumTopics
            channels.GetForumTopicsByID
    """

    __slots__: List[str] = ["flags", "count", "messages", "users"]

    ID = 0x367617d3
    QUALNAME = "types.messages.ForumTopics"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD order_by_create_date", count: "raw.base.int topics", messages: List["raw.base.Message> chat"], users: List["raw.base.User> pt"]) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD order_by_create_date
        self.count = count  # t.me/TheVenomXD int topics
        self.messages = messages  # t.me/TheVenomXD Vector<Message> chats
        self.users = users  # t.me/TheVenomXD Vector<User> pts

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ForumTopics":
        
        flags = TLObject.read(b)
        
        count = TLObject.read(b)
        
        messages = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return ForumTopics(flags=flags, count=count, messages=messages, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.count.write())
        
        b.write(Vector(self.messages))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
