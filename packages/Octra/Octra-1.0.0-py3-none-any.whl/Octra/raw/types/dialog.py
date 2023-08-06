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


class Dialog(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Dialog`.

    Details:
        - Layer: ``151``
        - ID: ``D58A08C6``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD pinned <Octra.raw.base.# t.me/TheVenomXD pinned>`):
            N/A

        top_message (:obj:`int read_inbox_max_id <Octra.raw.base.int read_inbox_max_id>`):
            N/A

        read_outbox_max_id (:obj:`int unread_count <Octra.raw.base.int unread_count>`):
            N/A

        unread_mentions_count (:obj:`int unread_reactions_count <Octra.raw.base.int unread_reactions_count>`):
            N/A

        notify_settings (:obj:`PeerNotifySettings pts <Octra.raw.base.PeerNotifySettings pts>`):
            N/A

        unread_mark (:obj:`true peer <Octra.raw.base.true peer>`, *optional*):
            N/A

        draft (:obj:`DraftMessage folder_id <Octra.raw.base.DraftMessage folder_id>`, *optional*):
            N/A

        ttl_period (:obj:`int  <Octra.raw.base.int >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "top_message", "read_outbox_max_id", "unread_mentions_count", "notify_settings", "unread_mark", "draft", "ttl_period"]

    ID = 0xd58a08c6
    QUALNAME = "types.Dialog"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD pinned", top_message: "raw.base.int read_inbox_max_id", read_outbox_max_id: "raw.base.int unread_count", unread_mentions_count: "raw.base.int unread_reactions_count", notify_settings: "raw.base.PeerNotifySettings pts", unread_mark: "raw.base.true peer" = None, draft: "raw.base.DraftMessage folder_id" = None, ttl_period: "raw.base.int " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD pinned
        self.top_message = top_message  # t.me/TheVenomXD int read_inbox_max_id
        self.read_outbox_max_id = read_outbox_max_id  # t.me/TheVenomXD int unread_count
        self.unread_mentions_count = unread_mentions_count  # t.me/TheVenomXD int unread_reactions_count
        self.notify_settings = notify_settings  # t.me/TheVenomXD PeerNotifySettings pts
        self.unread_mark = unread_mark  # t.me/TheVenomXD flags.3?true peer
        self.draft = draft  # t.me/TheVenomXD flags.1?DraftMessage folder_id
        self.ttl_period = ttl_period  # t.me/TheVenomXD flags.5?int 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Dialog":
        
        flags = TLObject.read(b)
        
        unread_mark = True if flags & (1 << 3) else False
        top_message = TLObject.read(b)
        
        read_outbox_max_id = TLObject.read(b)
        
        unread_mentions_count = TLObject.read(b)
        
        notify_settings = TLObject.read(b)
        
        draft = TLObject.read(b) if flags & (1 << 1) else None
        
        ttl_period = Int.read(b) if flags & (1 << 5) else None
        return Dialog(flags=flags, top_message=top_message, read_outbox_max_id=read_outbox_max_id, unread_mentions_count=unread_mentions_count, notify_settings=notify_settings, unread_mark=unread_mark, draft=draft, ttl_period=ttl_period)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.top_message.write())
        
        b.write(self.read_outbox_max_id.write())
        
        b.write(self.unread_mentions_count.write())
        
        b.write(self.notify_settings.write())
        
        if self.draft is not None:
            b.write(self.draft.write())
        
        if self.ttl_period is not None:
            b.write(Int(self.ttl_period))
        
        return b.getvalue()
