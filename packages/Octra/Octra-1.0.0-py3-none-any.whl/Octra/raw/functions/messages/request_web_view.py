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


class RequestWebView(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``178B480B``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD from_bot_menu <Octra.raw.base.# t.me/TheVenomXD from_bot_menu>`):
            N/A

        bot (:obj:`InputUser url <Octra.raw.base.InputUser url>`):
            N/A

        platform (:obj:`string reply_to_msg_id <Octra.raw.base.string reply_to_msg_id>`):
            N/A

        silent (:obj:`true peer <Octra.raw.base.true peer>`, *optional*):
            N/A

        start_param (:obj:`string theme_params <Octra.raw.base.string theme_params>`, *optional*):
            N/A

        top_msg_id (:obj:`int send_as <Octra.raw.base.int send_as>`, *optional*):
            N/A

    Returns:
        :obj:`WebViewResult <Octra.raw.base.WebViewResult>`
    """

    __slots__: List[str] = ["flags", "bot", "platform", "silent", "start_param", "top_msg_id"]

    ID = 0x178b480b
    QUALNAME = "functions.messages.RequestWebView"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD from_bot_menu", bot: "raw.base.InputUser url", platform: "raw.base.string reply_to_msg_id", silent: "raw.base.true peer" = None, start_param: "raw.base.string theme_params" = None, top_msg_id: "raw.base.int send_as" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD from_bot_menu
        self.bot = bot  # t.me/TheVenomXD InputUser url
        self.platform = platform  # t.me/TheVenomXD string reply_to_msg_id
        self.silent = silent  # t.me/TheVenomXD flags.5?true peer
        self.start_param = start_param  # t.me/TheVenomXD flags.3?string theme_params
        self.top_msg_id = top_msg_id  # t.me/TheVenomXD flags.9?int send_as

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "RequestWebView":
        
        flags = TLObject.read(b)
        
        silent = True if flags & (1 << 5) else False
        bot = TLObject.read(b)
        
        start_param = String.read(b) if flags & (1 << 3) else None
        platform = TLObject.read(b)
        
        top_msg_id = Int.read(b) if flags & (1 << 9) else None
        return RequestWebView(flags=flags, bot=bot, platform=platform, silent=silent, start_param=start_param, top_msg_id=top_msg_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.bot.write())
        
        if self.start_param is not None:
            b.write(String(self.start_param))
        
        b.write(self.platform.write())
        
        if self.top_msg_id is not None:
            b.write(Int(self.top_msg_id))
        
        return b.getvalue()
