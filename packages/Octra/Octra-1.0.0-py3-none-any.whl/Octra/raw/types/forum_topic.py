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


class ForumTopic(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.ForumTopic`.

    Details:
        - Layer: ``151``
        - ID: ``71701DA9``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD my <Octra.raw.base.# t.me/TheVenomXD my>`):
            N/A

        id (:obj:`int date <Octra.raw.base.int date>`):
            N/A

        title (:obj:`string icon_color <Octra.raw.base.string icon_color>`):
            N/A

        read_inbox_max_id (:obj:`int read_outbox_max_id <Octra.raw.base.int read_outbox_max_id>`):
            N/A

        unread_count (:obj:`int unread_mentions_count <Octra.raw.base.int unread_mentions_count>`):
            N/A

        unread_reactions_count (:obj:`int from_id <Octra.raw.base.int from_id>`):
            N/A

        notify_settings (:obj:`PeerNotifySettings draft <Octra.raw.base.PeerNotifySettings draft>`):
            N/A

        closed (:obj:`true pinned <Octra.raw.base.true pinned>`, *optional*):
            N/A

        short (:obj:`true hidden <Octra.raw.base.true hidden>`, *optional*):
            N/A

        icon_emoji_id (:obj:`long top_message <Octra.raw.base.long top_message>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "id", "title", "read_inbox_max_id", "unread_count", "unread_reactions_count", "notify_settings", "closed", "short", "icon_emoji_id"]

    ID = 0x71701da9
    QUALNAME = "types.ForumTopic"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD my", id: "raw.base.int date", title: "raw.base.string icon_color", read_inbox_max_id: "raw.base.int read_outbox_max_id", unread_count: "raw.base.int unread_mentions_count", unread_reactions_count: "raw.base.int from_id", notify_settings: "raw.base.PeerNotifySettings draft", closed: "raw.base.true pinned" = None, short: "raw.base.true hidden" = None, icon_emoji_id: "raw.base.long top_message" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD my
        self.id = id  # t.me/TheVenomXD int date
        self.title = title  # t.me/TheVenomXD string icon_color
        self.read_inbox_max_id = read_inbox_max_id  # t.me/TheVenomXD int read_outbox_max_id
        self.unread_count = unread_count  # t.me/TheVenomXD int unread_mentions_count
        self.unread_reactions_count = unread_reactions_count  # t.me/TheVenomXD int from_id
        self.notify_settings = notify_settings  # t.me/TheVenomXD PeerNotifySettings draft
        self.closed = closed  # t.me/TheVenomXD flags.2?true pinned
        self.short = short  # t.me/TheVenomXD flags.5?true hidden
        self.icon_emoji_id = icon_emoji_id  # t.me/TheVenomXD flags.0?long top_message

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ForumTopic":
        
        flags = TLObject.read(b)
        
        closed = True if flags & (1 << 2) else False
        short = True if flags & (1 << 5) else False
        id = TLObject.read(b)
        
        title = TLObject.read(b)
        
        icon_emoji_id = Long.read(b) if flags & (1 << 0) else None
        read_inbox_max_id = TLObject.read(b)
        
        unread_count = TLObject.read(b)
        
        unread_reactions_count = TLObject.read(b)
        
        notify_settings = TLObject.read(b)
        
        return ForumTopic(flags=flags, id=id, title=title, read_inbox_max_id=read_inbox_max_id, unread_count=unread_count, unread_reactions_count=unread_reactions_count, notify_settings=notify_settings, closed=closed, short=short, icon_emoji_id=icon_emoji_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.id.write())
        
        b.write(self.title.write())
        
        if self.icon_emoji_id is not None:
            b.write(Long(self.icon_emoji_id))
        
        b.write(self.read_inbox_max_id.write())
        
        b.write(self.unread_count.write())
        
        b.write(self.unread_reactions_count.write())
        
        b.write(self.notify_settings.write())
        
        return b.getvalue()
