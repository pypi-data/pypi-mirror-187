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


class MessageFwdHeader(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.MessageFwdHeader`.

    Details:
        - Layer: ``151``
        - ID: ``5F777DCE``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD imported <Octra.raw.base.# t.me/TheVenomXD imported>`):
            N/A

        date (:obj:`int channel_post <Octra.raw.base.int channel_post>`):
            N/A

        from_id (:obj:`Peer from_name <Octra.raw.base.Peer from_name>`, *optional*):
            N/A

        post_author (:obj:`string saved_from_peer <Octra.raw.base.string saved_from_peer>`, *optional*):
            N/A

        saved_from_msg_id (:obj:`int psa_type <Octra.raw.base.int psa_type>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "date", "from_id", "post_author", "saved_from_msg_id"]

    ID = 0x5f777dce
    QUALNAME = "types.MessageFwdHeader"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD imported", date: "raw.base.int channel_post", from_id: "raw.base.Peer from_name" = None, post_author: "raw.base.string saved_from_peer" = None, saved_from_msg_id: "raw.base.int psa_type" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD imported
        self.date = date  # t.me/TheVenomXD int channel_post
        self.from_id = from_id  # t.me/TheVenomXD flags.0?Peer from_name
        self.post_author = post_author  # t.me/TheVenomXD flags.3?string saved_from_peer
        self.saved_from_msg_id = saved_from_msg_id  # t.me/TheVenomXD flags.4?int psa_type

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageFwdHeader":
        
        flags = TLObject.read(b)
        
        from_id = TLObject.read(b) if flags & (1 << 0) else None
        
        date = TLObject.read(b)
        
        post_author = String.read(b) if flags & (1 << 3) else None
        saved_from_msg_id = Int.read(b) if flags & (1 << 4) else None
        return MessageFwdHeader(flags=flags, date=date, from_id=from_id, post_author=post_author, saved_from_msg_id=saved_from_msg_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.from_id is not None:
            b.write(self.from_id.write())
        
        b.write(self.date.write())
        
        if self.post_author is not None:
            b.write(String(self.post_author))
        
        if self.saved_from_msg_id is not None:
            b.write(Int(self.saved_from_msg_id))
        
        return b.getvalue()
