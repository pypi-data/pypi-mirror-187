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


class InitTakeoutSession(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``8EF3EAB0``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD contacts <Octra.raw.base.# t.me/TheVenomXD contacts>`):
            N/A

        message_users (:obj:`true message_chats <Octra.raw.base.true message_chats>`, *optional*):
            N/A

        message_megagroups (:obj:`true message_channels <Octra.raw.base.true message_channels>`, *optional*):
            N/A

        files (:obj:`true file_max_size <Octra.raw.base.true file_max_size>`, *optional*):
            N/A

    Returns:
        :obj:`account.Takeout <Octra.raw.base.account.Takeout>`
    """

    __slots__: List[str] = ["flags", "message_users", "message_megagroups", "files"]

    ID = 0x8ef3eab0
    QUALNAME = "functions.account.InitTakeoutSession"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD contacts", message_users: "raw.base.true message_chats" = None, message_megagroups: "raw.base.true message_channels" = None, files: "raw.base.true file_max_size" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD contacts
        self.message_users = message_users  # t.me/TheVenomXD flags.1?true message_chats
        self.message_megagroups = message_megagroups  # t.me/TheVenomXD flags.3?true message_channels
        self.files = files  # t.me/TheVenomXD flags.5?true file_max_size

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InitTakeoutSession":
        
        flags = TLObject.read(b)
        
        message_users = True if flags & (1 << 1) else False
        message_megagroups = True if flags & (1 << 3) else False
        files = True if flags & (1 << 5) else False
        return InitTakeoutSession(flags=flags, message_users=message_users, message_megagroups=message_megagroups, files=files)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        return b.getvalue()
