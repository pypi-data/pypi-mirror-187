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


class DialogFolder(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Dialog`.

    Details:
        - Layer: ``151``
        - ID: ``71BD134C``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD pinned <Octra.raw.base.# t.me/TheVenomXD pinned>`):
            N/A

        folder (:obj:`Folder peer <Octra.raw.base.Folder peer>`):
            N/A

        top_message (:obj:`int unread_muted_peers_count <Octra.raw.base.int unread_muted_peers_count>`):
            N/A

        unread_unmuted_peers_count (:obj:`int unread_muted_messages_count <Octra.raw.base.int unread_muted_messages_count>`):
            N/A

        unread_unmuted_messages_count (:obj:`int  <Octra.raw.base.int >`):
            N/A

    """

    __slots__: List[str] = ["flags", "folder", "top_message", "unread_unmuted_peers_count", "unread_unmuted_messages_count"]

    ID = 0x71bd134c
    QUALNAME = "types.DialogFolder"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD pinned", folder: "raw.base.Folder peer", top_message: "raw.base.int unread_muted_peers_count", unread_unmuted_peers_count: "raw.base.int unread_muted_messages_count", unread_unmuted_messages_count: "raw.base.int ") -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD pinned
        self.folder = folder  # t.me/TheVenomXD Folder peer
        self.top_message = top_message  # t.me/TheVenomXD int unread_muted_peers_count
        self.unread_unmuted_peers_count = unread_unmuted_peers_count  # t.me/TheVenomXD int unread_muted_messages_count
        self.unread_unmuted_messages_count = unread_unmuted_messages_count  # t.me/TheVenomXD int 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DialogFolder":
        
        flags = TLObject.read(b)
        
        folder = TLObject.read(b)
        
        top_message = TLObject.read(b)
        
        unread_unmuted_peers_count = TLObject.read(b)
        
        unread_unmuted_messages_count = TLObject.read(b)
        
        return DialogFolder(flags=flags, folder=folder, top_message=top_message, unread_unmuted_peers_count=unread_unmuted_peers_count, unread_unmuted_messages_count=unread_unmuted_messages_count)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.folder.write())
        
        b.write(self.top_message.write())
        
        b.write(self.unread_unmuted_peers_count.write())
        
        b.write(self.unread_unmuted_messages_count.write())
        
        return b.getvalue()
