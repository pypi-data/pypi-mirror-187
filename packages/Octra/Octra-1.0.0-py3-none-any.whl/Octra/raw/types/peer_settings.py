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


class PeerSettings(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.PeerSettings`.

    Details:
        - Layer: ``151``
        - ID: ``A518110D``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD report_spam <Octra.raw.base.# t.me/TheVenomXD report_spam>`):
            N/A

        add_contact (:obj:`true block_contact <Octra.raw.base.true block_contact>`, *optional*):
            N/A

        share_contact (:obj:`true need_contacts_exception <Octra.raw.base.true need_contacts_exception>`, *optional*):
            N/A

        report_geo (:obj:`true autoarchived <Octra.raw.base.true autoarchived>`, *optional*):
            N/A

        invite_USERs (:obj:`true request_chat_broadcast <Octra.raw.base.true request_chat_broadcast>`, *optional*):
            N/A

        geo_distance (:obj:`int request_chat_title <Octra.raw.base.int request_chat_title>`, *optional*):
            N/A

        request_chat_date (:obj:`int  <Octra.raw.base.int >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "add_contact", "share_contact", "report_geo", "invite_USERs", "geo_distance", "request_chat_date"]

    ID = 0xa518110d
    QUALNAME = "types.PeerSettings"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD report_spam", add_contact: "raw.base.true block_contact" = None, share_contact: "raw.base.true need_contacts_exception" = None, report_geo: "raw.base.true autoarchived" = None, invite_USERs: "raw.base.true request_chat_broadcast" = None, geo_distance: "raw.base.int request_chat_title" = None, request_chat_date: "raw.base.int " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD report_spam
        self.add_contact = add_contact  # t.me/TheVenomXD flags.1?true block_contact
        self.share_contact = share_contact  # t.me/TheVenomXD flags.3?true need_contacts_exception
        self.report_geo = report_geo  # t.me/TheVenomXD flags.5?true autoarchived
        self.invite_USERs = invite_USERs  # t.me/TheVenomXD flags.8?true request_chat_broadcast
        self.geo_distance = geo_distance  # t.me/TheVenomXD flags.6?int request_chat_title
        self.request_chat_date = request_chat_date  # t.me/TheVenomXD flags.9?int 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PeerSettings":
        
        flags = TLObject.read(b)
        
        add_contact = True if flags & (1 << 1) else False
        share_contact = True if flags & (1 << 3) else False
        report_geo = True if flags & (1 << 5) else False
        invite_USERs = True if flags & (1 << 8) else False
        geo_distance = Int.read(b) if flags & (1 << 6) else None
        request_chat_date = Int.read(b) if flags & (1 << 9) else None
        return PeerSettings(flags=flags, add_contact=add_contact, share_contact=share_contact, report_geo=report_geo, invite_USERs=invite_USERs, geo_distance=geo_distance, request_chat_date=request_chat_date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.geo_distance is not None:
            b.write(Int(self.geo_distance))
        
        if self.request_chat_date is not None:
            b.write(Int(self.request_chat_date))
        
        return b.getvalue()
