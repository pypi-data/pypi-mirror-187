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


class ChatBannedRights(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.ChatBannedRights`.

    Details:
        - Layer: ``151``
        - ID: ``9F120418``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD view_messages <Octra.raw.base.# t.me/TheVenomXD view_messages>`):
            N/A

        until_date (:obj:`int  <Octra.raw.base.int >`):
            N/A

        send_messages (:obj:`true send_media <Octra.raw.base.true send_media>`, *optional*):
            N/A

        send_stickers (:obj:`true send_gifs <Octra.raw.base.true send_gifs>`, *optional*):
            N/A

        send_games (:obj:`true send_inline <Octra.raw.base.true send_inline>`, *optional*):
            N/A

        embed_links (:obj:`true send_polls <Octra.raw.base.true send_polls>`, *optional*):
            N/A

        change_info (:obj:`true invite_users <Octra.raw.base.true invite_users>`, *optional*):
            N/A

        pin_messages (:obj:`true manage_topics <Octra.raw.base.true manage_topics>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "until_date", "send_messages", "send_stickers", "send_games", "embed_links", "change_info", "pin_messages"]

    ID = 0x9f120418
    QUALNAME = "types.ChatBannedRights"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD view_messages", until_date: "raw.base.int ", send_messages: "raw.base.true send_media" = None, send_stickers: "raw.base.true send_gifs" = None, send_games: "raw.base.true send_inline" = None, embed_links: "raw.base.true send_polls" = None, change_info: "raw.base.true invite_users" = None, pin_messages: "raw.base.true manage_topics" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD view_messages
        self.until_date = until_date  # t.me/TheVenomXD int 
        self.send_messages = send_messages  # t.me/TheVenomXD flags.1?true send_media
        self.send_stickers = send_stickers  # t.me/TheVenomXD flags.3?true send_gifs
        self.send_games = send_games  # t.me/TheVenomXD flags.5?true send_inline
        self.embed_links = embed_links  # t.me/TheVenomXD flags.7?true send_polls
        self.change_info = change_info  # t.me/TheVenomXD flags.10?true invite_users
        self.pin_messages = pin_messages  # t.me/TheVenomXD flags.17?true manage_topics

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChatBannedRights":
        
        flags = TLObject.read(b)
        
        send_messages = True if flags & (1 << 1) else False
        send_stickers = True if flags & (1 << 3) else False
        send_games = True if flags & (1 << 5) else False
        embed_links = True if flags & (1 << 7) else False
        change_info = True if flags & (1 << 10) else False
        pin_messages = True if flags & (1 << 17) else False
        until_date = TLObject.read(b)
        
        return ChatBannedRights(flags=flags, until_date=until_date, send_messages=send_messages, send_stickers=send_stickers, send_games=send_games, embed_links=embed_links, change_info=change_info, pin_messages=pin_messages)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.until_date.write())
        
        return b.getvalue()
