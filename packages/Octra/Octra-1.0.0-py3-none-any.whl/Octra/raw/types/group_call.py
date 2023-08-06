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


class GroupCall(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.GroupCall`.

    Details:
        - Layer: ``151``
        - ID: ``D597650C``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD join_muted <Octra.raw.base.# t.me/TheVenomXD join_muted>`):
            N/A

        access_hash (:obj:`long participants_count <Octra.raw.base.long participants_count>`):
            N/A

        version (:obj:`int  <Octra.raw.base.int >`):
            N/A

        can_change_join_muted (:obj:`true join_date_asc <Octra.raw.base.true join_date_asc>`, *optional*):
            N/A

        schedule_start_subscribed (:obj:`true can_start_video <Octra.raw.base.true can_start_video>`, *optional*):
            N/A

        record_video_active (:obj:`true rtmp_stream <Octra.raw.base.true rtmp_stream>`, *optional*):
            N/A

        listeners_hidden (:obj:`true id <Octra.raw.base.true id>`, *optional*):
            N/A

        title (:obj:`string stream_octra_dc_id_ <Octra.raw.base.string stream_octra_dc_id_>`, *optional*):
            N/A

        record_start_date (:obj:`int schedule_date <Octra.raw.base.int schedule_date>`, *optional*):
            N/A

        unmuted_video_count (:obj:`int unmuted_video_limit <Octra.raw.base.int unmuted_video_limit>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "access_hash", "version", "can_change_join_muted", "schedule_start_subscribed", "record_video_active", "listeners_hidden", "title", "record_start_date", "unmuted_video_count"]

    ID = 0xd597650c
    QUALNAME = "types.GroupCall"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD join_muted", access_hash: "raw.base.long participants_count", version: "raw.base.int ", can_change_join_muted: "raw.base.true join_date_asc" = None, schedule_start_subscribed: "raw.base.true can_start_video" = None, record_video_active: "raw.base.true rtmp_stream" = None, listeners_hidden: "raw.base.true id" = None, title: "raw.base.string stream_octra_dc_id_" = None, record_start_date: "raw.base.int schedule_date" = None, unmuted_video_count: "raw.base.int unmuted_video_limit" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD join_muted
        self.access_hash = access_hash  # t.me/TheVenomXD long participants_count
        self.version = version  # t.me/TheVenomXD int 
        self.can_change_join_muted = can_change_join_muted  # t.me/TheVenomXD flags.2?true join_date_asc
        self.schedule_start_subscribed = schedule_start_subscribed  # t.me/TheVenomXD flags.8?true can_start_video
        self.record_video_active = record_video_active  # t.me/TheVenomXD flags.11?true rtmp_stream
        self.listeners_hidden = listeners_hidden  # t.me/TheVenomXD flags.13?true id
        self.title = title  # t.me/TheVenomXD flags.3?string stream_octra_dc_id_
        self.record_start_date = record_start_date  # t.me/TheVenomXD flags.5?int schedule_date
        self.unmuted_video_count = unmuted_video_count  # t.me/TheVenomXD flags.10?int unmuted_video_limit

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GroupCall":
        
        flags = TLObject.read(b)
        
        can_change_join_muted = True if flags & (1 << 2) else False
        schedule_start_subscribed = True if flags & (1 << 8) else False
        record_video_active = True if flags & (1 << 11) else False
        listeners_hidden = True if flags & (1 << 13) else False
        access_hash = TLObject.read(b)
        
        title = String.read(b) if flags & (1 << 3) else None
        record_start_date = Int.read(b) if flags & (1 << 5) else None
        unmuted_video_count = Int.read(b) if flags & (1 << 10) else None
        version = TLObject.read(b)
        
        return GroupCall(flags=flags, access_hash=access_hash, version=version, can_change_join_muted=can_change_join_muted, schedule_start_subscribed=schedule_start_subscribed, record_video_active=record_video_active, listeners_hidden=listeners_hidden, title=title, record_start_date=record_start_date, unmuted_video_count=unmuted_video_count)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.access_hash.write())
        
        if self.title is not None:
            b.write(String(self.title))
        
        if self.record_start_date is not None:
            b.write(Int(self.record_start_date))
        
        if self.unmuted_video_count is not None:
            b.write(Int(self.unmuted_video_count))
        
        b.write(self.version.write())
        
        return b.getvalue()
