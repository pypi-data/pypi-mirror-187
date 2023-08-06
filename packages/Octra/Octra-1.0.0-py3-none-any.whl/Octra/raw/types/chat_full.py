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


class ChatFull(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.ChatFull`.

    Details:
        - Layer: ``151``
        - ID: ``C9D31138``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD can_set_username <Octra.raw.base.# t.me/TheVenomXD can_set_username>`):
            N/A

        about (:obj:`string participants <Octra.raw.base.string participants>`):
            N/A

        has_scheduled (:obj:`true id <Octra.raw.base.true id>`, *optional*):
            N/A

        chat_photo (:obj:`Photo notify_settings <Octra.raw.base.Photo notify_settings>`, *optional*):
            N/A

        exported_invite (:obj:`ExportedChatInvite bot_info <Octra.raw.base.ExportedChatInvite bot_info>`, *optional*):
            N/A

        pinned_msg_id (:obj:`int folder_id <Octra.raw.base.int folder_id>`, *optional*):
            N/A

        call (:obj:`InputGroupCall ttl_period <Octra.raw.base.InputGroupCall ttl_period>`, *optional*):
            N/A

        groupcall_default_join_as (:obj:`Peer theme_emoticon <Octra.raw.base.Peer theme_emoticon>`, *optional*):
            N/A

        requests_pending (:obj:`int recent_requesters <Octra.raw.base.int recent_requesters>`, *optional*):
            N/A

        available_reactions (:obj:`ChatReactions  <Octra.raw.base.ChatReactions >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "about", "has_scheduled", "chat_photo", "exported_invite", "pinned_msg_id", "call", "groupcall_default_join_as", "requests_pending", "available_reactions"]

    ID = 0xc9d31138
    QUALNAME = "types.ChatFull"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD can_set_username", about: "raw.base.string participants", has_scheduled: "raw.base.true id" = None, chat_photo: "raw.base.Photo notify_settings" = None, exported_invite: "raw.base.ExportedChatInvite bot_info" = None, pinned_msg_id: "raw.base.int folder_id" = None, call: "raw.base.InputGroupCall ttl_period" = None, groupcall_default_join_as: "raw.base.Peer theme_emoticon" = None, requests_pending: "raw.base.int recent_requesters" = None, available_reactions: "raw.base.ChatReactions " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD can_set_username
        self.about = about  # t.me/TheVenomXD string participants
        self.has_scheduled = has_scheduled  # t.me/TheVenomXD flags.8?true id
        self.chat_photo = chat_photo  # t.me/TheVenomXD flags.2?Photo notify_settings
        self.exported_invite = exported_invite  # t.me/TheVenomXD flags.13?ExportedChatInvite bot_info
        self.pinned_msg_id = pinned_msg_id  # t.me/TheVenomXD flags.6?int folder_id
        self.call = call  # t.me/TheVenomXD flags.12?InputGroupCall ttl_period
        self.groupcall_default_join_as = groupcall_default_join_as  # t.me/TheVenomXD flags.15?Peer theme_emoticon
        self.requests_pending = requests_pending  # t.me/TheVenomXD flags.17?int recent_requesters
        self.available_reactions = available_reactions  # t.me/TheVenomXD flags.18?ChatReactions 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChatFull":
        
        flags = TLObject.read(b)
        
        has_scheduled = True if flags & (1 << 8) else False
        about = TLObject.read(b)
        
        chat_photo = TLObject.read(b) if flags & (1 << 2) else None
        
        exported_invite = TLObject.read(b) if flags & (1 << 13) else None
        
        pinned_msg_id = Int.read(b) if flags & (1 << 6) else None
        call = TLObject.read(b) if flags & (1 << 12) else None
        
        groupcall_default_join_as = TLObject.read(b) if flags & (1 << 15) else None
        
        requests_pending = Int.read(b) if flags & (1 << 17) else None
        available_reactions = TLObject.read(b) if flags & (1 << 18) else None
        
        return ChatFull(flags=flags, about=about, has_scheduled=has_scheduled, chat_photo=chat_photo, exported_invite=exported_invite, pinned_msg_id=pinned_msg_id, call=call, groupcall_default_join_as=groupcall_default_join_as, requests_pending=requests_pending, available_reactions=available_reactions)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.about.write())
        
        if self.chat_photo is not None:
            b.write(self.chat_photo.write())
        
        if self.exported_invite is not None:
            b.write(self.exported_invite.write())
        
        if self.pinned_msg_id is not None:
            b.write(Int(self.pinned_msg_id))
        
        if self.call is not None:
            b.write(self.call.write())
        
        if self.groupcall_default_join_as is not None:
            b.write(self.groupcall_default_join_as.write())
        
        if self.requests_pending is not None:
            b.write(Int(self.requests_pending))
        
        if self.available_reactions is not None:
            b.write(self.available_reactions.write())
        
        return b.getvalue()
