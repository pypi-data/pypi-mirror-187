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


class ChatAdminRights(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.ChatAdminRights`.

    Details:
        - Layer: ``151``
        - ID: ``5FB224D5``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD change_info <Octra.raw.base.# t.me/TheVenomXD change_info>`):
            N/A

        post_messages (:obj:`true edit_messages <Octra.raw.base.true edit_messages>`, *optional*):
            N/A

        delete_messages (:obj:`true ban_users <Octra.raw.base.true ban_users>`, *optional*):
            N/A

        invite_users (:obj:`true pin_messages <Octra.raw.base.true pin_messages>`, *optional*):
            N/A

        add_admins (:obj:`true anonymous <Octra.raw.base.true anonymous>`, *optional*):
            N/A

        manage_call (:obj:`true other <Octra.raw.base.true other>`, *optional*):
            N/A

        manage_topics (:obj:`true  <Octra.raw.base.true >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "post_messages", "delete_messages", "invite_users", "add_admins", "manage_call", "manage_topics"]

    ID = 0x5fb224d5
    QUALNAME = "types.ChatAdminRights"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD change_info", post_messages: "raw.base.true edit_messages" = None, delete_messages: "raw.base.true ban_users" = None, invite_users: "raw.base.true pin_messages" = None, add_admins: "raw.base.true anonymous" = None, manage_call: "raw.base.true other" = None, manage_topics: "raw.base.true " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD change_info
        self.post_messages = post_messages  # t.me/TheVenomXD flags.1?true edit_messages
        self.delete_messages = delete_messages  # t.me/TheVenomXD flags.3?true ban_users
        self.invite_users = invite_users  # t.me/TheVenomXD flags.5?true pin_messages
        self.add_admins = add_admins  # t.me/TheVenomXD flags.9?true anonymous
        self.manage_call = manage_call  # t.me/TheVenomXD flags.11?true other
        self.manage_topics = manage_topics  # t.me/TheVenomXD flags.13?true 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChatAdminRights":
        
        flags = TLObject.read(b)
        
        post_messages = True if flags & (1 << 1) else False
        delete_messages = True if flags & (1 << 3) else False
        invite_users = True if flags & (1 << 5) else False
        add_admins = True if flags & (1 << 9) else False
        manage_call = True if flags & (1 << 11) else False
        manage_topics = True if flags & (1 << 13) else False
        return ChatAdminRights(flags=flags, post_messages=post_messages, delete_messages=delete_messages, invite_users=invite_users, add_admins=add_admins, manage_call=manage_call, manage_topics=manage_topics)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        return b.getvalue()
