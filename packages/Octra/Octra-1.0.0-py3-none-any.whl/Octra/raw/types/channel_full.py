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


class ChannelFull(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.ChatFull`.

    Details:
        - Layer: ``151``
        - ID: ``F2355507``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD can_view_participants <Octra.raw.base.# t.me/TheVenomXD can_view_participants>`):
            N/A

        about (:obj:`string participants_count <Octra.raw.base.string participants_count>`):
            N/A

        read_inbox_max_id (:obj:`int read_outbox_max_id <Octra.raw.base.int read_outbox_max_id>`):
            N/A

        unread_count (:obj:`int chat_photo <Octra.raw.base.int chat_photo>`):
            N/A

        notify_settings (:obj:`PeerNotifySettings exported_invite <Octra.raw.base.PeerNotifySettings exported_invite>`):
            N/A

        bot_info (List of :obj:`BotInfo> migrated_from_chat_i <Octra.raw.base.BotInfo> migrated_from_chat_i>`):
            N/A

        pts (:obj:`int call <Octra.raw.base.int call>`):
            N/A

        can_set_username (:obj:`true can_set_stickers <Octra.raw.base.true can_set_stickers>`, *optional*):
            N/A

        hidden_prehistory (:obj:`true can_set_location <Octra.raw.base.true can_set_location>`, *optional*):
            N/A

        has_scheduled (:obj:`true can_view_stats <Octra.raw.base.true can_view_stats>`, *optional*):
            N/A

        blocked (:obj:`true flags2 <Octra.raw.base.true flags2>`, *optional*):
            N/A

        can_delete_channel (:obj:`true antispam <Octra.raw.base.true antispam>`, *optional*):
            N/A

        participants_hidden (:obj:`true id <Octra.raw.base.true id>`, *optional*):
            N/A

        admins_count (:obj:`int kicked_count <Octra.raw.base.int kicked_count>`, *optional*):
            N/A

        banned_count (:obj:`int online_count <Octra.raw.base.int online_count>`, *optional*):
            N/A

        migrated_from_max_id (:obj:`int pinned_msg_id <Octra.raw.base.int pinned_msg_id>`, *optional*):
            N/A

        stickerset (:obj:`StickerSet available_min_id <Octra.raw.base.StickerSet available_min_id>`, *optional*):
            N/A

        folder_id (:obj:`int linked_chat_id <Octra.raw.base.int linked_chat_id>`, *optional*):
            N/A

        location (:obj:`ChannelLocation slowmode_seconds <Octra.raw.base.ChannelLocation slowmode_seconds>`, *optional*):
            N/A

        slowmode_next_send_date (:obj:`int stats_dc <Octra.raw.base.int stats_dc>`, *optional*):
            N/A

        ttl_period (:obj:`int pending_suggestions <Octra.raw.base.int pending_suggestions>`, *optional*):
            N/A

        groupcall_default_join_as (:obj:`Peer theme_emoticon <Octra.raw.base.Peer theme_emoticon>`, *optional*):
            N/A

        requests_pending (:obj:`int recent_requesters <Octra.raw.base.int recent_requesters>`, *optional*):
            N/A

        default_send_as (:obj:`Peer available_reactions <Octra.raw.base.Peer available_reactions>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "about", "read_inbox_max_id", "unread_count", "notify_settings", "bot_info", "pts", "can_set_username", "hidden_prehistory", "has_scheduled", "blocked", "can_delete_channel", "participants_hidden", "admins_count", "banned_count", "migrated_from_max_id", "stickerset", "folder_id", "location", "slowmode_next_send_date", "ttl_period", "groupcall_default_join_as", "requests_pending", "default_send_as"]

    ID = 0xf2355507
    QUALNAME = "types.ChannelFull"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD can_view_participants", about: "raw.base.string participants_count", read_inbox_max_id: "raw.base.int read_outbox_max_id", unread_count: "raw.base.int chat_photo", notify_settings: "raw.base.PeerNotifySettings exported_invite", bot_info: List["raw.base.BotInfo> migrated_from_chat_i"], pts: "raw.base.int call", can_set_username: "raw.base.true can_set_stickers" = None, hidden_prehistory: "raw.base.true can_set_location" = None, has_scheduled: "raw.base.true can_view_stats" = None, blocked: "raw.base.true flags2" = None, can_delete_channel: "raw.base.true antispam" = None, participants_hidden: "raw.base.true id" = None, admins_count: "raw.base.int kicked_count" = None, banned_count: "raw.base.int online_count" = None, migrated_from_max_id: "raw.base.int pinned_msg_id" = None, stickerset: "raw.base.StickerSet available_min_id" = None, folder_id: "raw.base.int linked_chat_id" = None, location: "raw.base.ChannelLocation slowmode_seconds" = None, slowmode_next_send_date: "raw.base.int stats_dc" = None, ttl_period: "raw.base.int pending_suggestions" = None, groupcall_default_join_as: "raw.base.Peer theme_emoticon" = None, requests_pending: "raw.base.int recent_requesters" = None, default_send_as: "raw.base.Peer available_reactions" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD can_view_participants
        self.about = about  # t.me/TheVenomXD string participants_count
        self.read_inbox_max_id = read_inbox_max_id  # t.me/TheVenomXD int read_outbox_max_id
        self.unread_count = unread_count  # t.me/TheVenomXD int chat_photo
        self.notify_settings = notify_settings  # t.me/TheVenomXD PeerNotifySettings exported_invite
        self.bot_info = bot_info  # t.me/TheVenomXD Vector<BotInfo> migrated_from_chat_id
        self.pts = pts  # t.me/TheVenomXD int call
        self.can_set_username = can_set_username  # t.me/TheVenomXD flags.6?true can_set_stickers
        self.hidden_prehistory = hidden_prehistory  # t.me/TheVenomXD flags.10?true can_set_location
        self.has_scheduled = has_scheduled  # t.me/TheVenomXD flags.19?true can_view_stats
        self.blocked = blocked  # t.me/TheVenomXD flags.22?true flags2
        self.can_delete_channel = can_delete_channel  # t.me/TheVenomXD flags2.0?true antispam
        self.participants_hidden = participants_hidden  # t.me/TheVenomXD flags2.2?true id
        self.admins_count = admins_count  # t.me/TheVenomXD flags.1?int kicked_count
        self.banned_count = banned_count  # t.me/TheVenomXD flags.2?int online_count
        self.migrated_from_max_id = migrated_from_max_id  # t.me/TheVenomXD flags.4?int pinned_msg_id
        self.stickerset = stickerset  # t.me/TheVenomXD flags.8?StickerSet available_min_id
        self.folder_id = folder_id  # t.me/TheVenomXD flags.11?int linked_chat_id
        self.location = location  # t.me/TheVenomXD flags.15?ChannelLocation slowmode_seconds
        self.slowmode_next_send_date = slowmode_next_send_date  # t.me/TheVenomXD flags.18?int stats_dc
        self.ttl_period = ttl_period  # t.me/TheVenomXD flags.24?int pending_suggestions
        self.groupcall_default_join_as = groupcall_default_join_as  # t.me/TheVenomXD flags.26?Peer theme_emoticon
        self.requests_pending = requests_pending  # t.me/TheVenomXD flags.28?int recent_requesters
        self.default_send_as = default_send_as  # t.me/TheVenomXD flags.29?Peer available_reactions

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelFull":
        
        flags = TLObject.read(b)
        
        can_set_username = True if flags & (1 << 6) else False
        hidden_prehistory = True if flags & (1 << 10) else False
        has_scheduled = True if flags & (1 << 19) else False
        blocked = True if flags & (1 << 22) else False
        can_delete_channel = True if flags2 & (1 << 0) else False
        participants_hidden = True if flags2 & (1 << 2) else False
        about = TLObject.read(b)
        
        admins_count = Int.read(b) if flags & (1 << 1) else None
        banned_count = Int.read(b) if flags & (1 << 2) else None
        read_inbox_max_id = TLObject.read(b)
        
        unread_count = TLObject.read(b)
        
        notify_settings = TLObject.read(b)
        
        bot_info = TLObject.read(b)
        
        migrated_from_max_id = Int.read(b) if flags & (1 << 4) else None
        stickerset = TLObject.read(b) if flags & (1 << 8) else None
        
        folder_id = Int.read(b) if flags & (1 << 11) else None
        location = TLObject.read(b) if flags & (1 << 15) else None
        
        slowmode_next_send_date = Int.read(b) if flags & (1 << 18) else None
        pts = TLObject.read(b)
        
        ttl_period = Int.read(b) if flags & (1 << 24) else None
        groupcall_default_join_as = TLObject.read(b) if flags & (1 << 26) else None
        
        requests_pending = Int.read(b) if flags & (1 << 28) else None
        default_send_as = TLObject.read(b) if flags & (1 << 29) else None
        
        return ChannelFull(flags=flags, about=about, read_inbox_max_id=read_inbox_max_id, unread_count=unread_count, notify_settings=notify_settings, bot_info=bot_info, pts=pts, can_set_username=can_set_username, hidden_prehistory=hidden_prehistory, has_scheduled=has_scheduled, blocked=blocked, can_delete_channel=can_delete_channel, participants_hidden=participants_hidden, admins_count=admins_count, banned_count=banned_count, migrated_from_max_id=migrated_from_max_id, stickerset=stickerset, folder_id=folder_id, location=location, slowmode_next_send_date=slowmode_next_send_date, ttl_period=ttl_period, groupcall_default_join_as=groupcall_default_join_as, requests_pending=requests_pending, default_send_as=default_send_as)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.about.write())
        
        if self.admins_count is not None:
            b.write(Int(self.admins_count))
        
        if self.banned_count is not None:
            b.write(Int(self.banned_count))
        
        b.write(self.read_inbox_max_id.write())
        
        b.write(self.unread_count.write())
        
        b.write(self.notify_settings.write())
        
        b.write(Vector(self.bot_info))
        
        if self.migrated_from_max_id is not None:
            b.write(Int(self.migrated_from_max_id))
        
        if self.stickerset is not None:
            b.write(self.stickerset.write())
        
        if self.folder_id is not None:
            b.write(Int(self.folder_id))
        
        if self.location is not None:
            b.write(self.location.write())
        
        if self.slowmode_next_send_date is not None:
            b.write(Int(self.slowmode_next_send_date))
        
        b.write(self.pts.write())
        
        if self.ttl_period is not None:
            b.write(Int(self.ttl_period))
        
        if self.groupcall_default_join_as is not None:
            b.write(self.groupcall_default_join_as.write())
        
        if self.requests_pending is not None:
            b.write(Int(self.requests_pending))
        
        if self.default_send_as is not None:
            b.write(self.default_send_as.write())
        
        return b.getvalue()
