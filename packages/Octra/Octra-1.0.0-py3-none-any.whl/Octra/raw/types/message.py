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


class Message(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Message`.

    Details:
        - Layer: ``151``
        - ID: ``38116EE0``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD out <Octra.raw.base.# t.me/TheVenomXD out>`):
            N/A

        message (:obj:`string media <Octra.raw.base.string media>`):
            N/A

        mentioned (:obj:`true media_unread <Octra.raw.base.true media_unread>`, *optional*):
            N/A

        silent (:obj:`true post <Octra.raw.base.true post>`, *optional*):
            N/A

        from_scheduled (:obj:`true legacy <Octra.raw.base.true legacy>`, *optional*):
            N/A

        edit_hide (:obj:`true pinned <Octra.raw.base.true pinned>`, *optional*):
            N/A

        noforwards (:obj:`true id <Octra.raw.base.true id>`, *optional*):
            N/A

        from_id (:obj:`Peer peer_id <Octra.raw.base.Peer peer_id>`, *optional*):
            N/A

        fwd_from (:obj:`MessageFwdHeader via_bot_id <Octra.raw.base.MessageFwdHeader via_bot_id>`, *optional*):
            N/A

        reply_to (:obj:`MessageReplyHeader date <Octra.raw.base.MessageReplyHeader date>`, *optional*):
            N/A

        reply_markup (:obj:`ReplyMarkup entities <Octra.raw.base.ReplyMarkup entities>`, *optional*):
            N/A

        views (:obj:`int forwards <Octra.raw.base.int forwards>`, *optional*):
            N/A

        replies (:obj:`MessageReplies edit_date <Octra.raw.base.MessageReplies edit_date>`, *optional*):
            N/A

        post_author (:obj:`string grouped_id <Octra.raw.base.string grouped_id>`, *optional*):
            N/A

        reactions (:obj:`MessageReactions restriction_reason <Octra.raw.base.MessageReactions restriction_reason>`, *optional*):
            N/A

        ttl_period (:obj:`int  <Octra.raw.base.int >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "message", "mentioned", "silent", "from_scheduled", "edit_hide", "noforwards", "from_id", "fwd_from", "reply_to", "reply_markup", "views", "replies", "post_author", "reactions", "ttl_period"]

    ID = 0x38116ee0
    QUALNAME = "types.Message"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD out", message: "raw.base.string media", mentioned: "raw.base.true media_unread" = None, silent: "raw.base.true post" = None, from_scheduled: "raw.base.true legacy" = None, edit_hide: "raw.base.true pinned" = None, noforwards: "raw.base.true id" = None, from_id: "raw.base.Peer peer_id" = None, fwd_from: "raw.base.MessageFwdHeader via_bot_id" = None, reply_to: "raw.base.MessageReplyHeader date" = None, reply_markup: "raw.base.ReplyMarkup entities" = None, views: "raw.base.int forwards" = None, replies: "raw.base.MessageReplies edit_date" = None, post_author: "raw.base.string grouped_id" = None, reactions: "raw.base.MessageReactions restriction_reason" = None, ttl_period: "raw.base.int " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD out
        self.message = message  # t.me/TheVenomXD string media
        self.mentioned = mentioned  # t.me/TheVenomXD flags.4?true media_unread
        self.silent = silent  # t.me/TheVenomXD flags.13?true post
        self.from_scheduled = from_scheduled  # t.me/TheVenomXD flags.18?true legacy
        self.edit_hide = edit_hide  # t.me/TheVenomXD flags.21?true pinned
        self.noforwards = noforwards  # t.me/TheVenomXD flags.26?true id
        self.from_id = from_id  # t.me/TheVenomXD flags.8?Peer peer_id
        self.fwd_from = fwd_from  # t.me/TheVenomXD flags.2?MessageFwdHeader via_bot_id
        self.reply_to = reply_to  # t.me/TheVenomXD flags.3?MessageReplyHeader date
        self.reply_markup = reply_markup  # t.me/TheVenomXD flags.6?ReplyMarkup entities
        self.views = views  # t.me/TheVenomXD flags.10?int forwards
        self.replies = replies  # t.me/TheVenomXD flags.23?MessageReplies edit_date
        self.post_author = post_author  # t.me/TheVenomXD flags.16?string grouped_id
        self.reactions = reactions  # t.me/TheVenomXD flags.20?MessageReactions restriction_reason
        self.ttl_period = ttl_period  # t.me/TheVenomXD flags.25?int 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Message":
        
        flags = TLObject.read(b)
        
        mentioned = True if flags & (1 << 4) else False
        silent = True if flags & (1 << 13) else False
        from_scheduled = True if flags & (1 << 18) else False
        edit_hide = True if flags & (1 << 21) else False
        noforwards = True if flags & (1 << 26) else False
        from_id = TLObject.read(b) if flags & (1 << 8) else None
        
        fwd_from = TLObject.read(b) if flags & (1 << 2) else None
        
        reply_to = TLObject.read(b) if flags & (1 << 3) else None
        
        message = TLObject.read(b)
        
        reply_markup = TLObject.read(b) if flags & (1 << 6) else None
        
        views = Int.read(b) if flags & (1 << 10) else None
        replies = TLObject.read(b) if flags & (1 << 23) else None
        
        post_author = String.read(b) if flags & (1 << 16) else None
        reactions = TLObject.read(b) if flags & (1 << 20) else None
        
        ttl_period = Int.read(b) if flags & (1 << 25) else None
        return Message(flags=flags, message=message, mentioned=mentioned, silent=silent, from_scheduled=from_scheduled, edit_hide=edit_hide, noforwards=noforwards, from_id=from_id, fwd_from=fwd_from, reply_to=reply_to, reply_markup=reply_markup, views=views, replies=replies, post_author=post_author, reactions=reactions, ttl_period=ttl_period)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.from_id is not None:
            b.write(self.from_id.write())
        
        if self.fwd_from is not None:
            b.write(self.fwd_from.write())
        
        if self.reply_to is not None:
            b.write(self.reply_to.write())
        
        b.write(self.message.write())
        
        if self.reply_markup is not None:
            b.write(self.reply_markup.write())
        
        if self.views is not None:
            b.write(Int(self.views))
        
        if self.replies is not None:
            b.write(self.replies.write())
        
        if self.post_author is not None:
            b.write(String(self.post_author))
        
        if self.reactions is not None:
            b.write(self.reactions.write())
        
        if self.ttl_period is not None:
            b.write(Int(self.ttl_period))
        
        return b.getvalue()
