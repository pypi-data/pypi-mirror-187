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


class UpdateInlineBotCallbackQuery(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Update`.

    Details:
        - Layer: ``151``
        - ID: ``691E9052``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD query_id <Octra.raw.base.# t.me/TheVenomXD query_id>`):
            N/A

        octra_user_id (:obj:`long msg_id <Octra.raw.base.long msg_id>`):
            N/A

        chat_instance (:obj:`long data <Octra.raw.base.long data>`):
            N/A

        game_short_name (:obj:`string  <Octra.raw.base.string >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "octra_user_id", "chat_instance", "game_short_name"]

    ID = 0x691e9052
    QUALNAME = "types.UpdateInlineBotCallbackQuery"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD query_id", octra_user_id: "raw.base.long msg_id", chat_instance: "raw.base.long data", game_short_name: "raw.base.string " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD query_id
        self.octra_user_id = octra_user_id  # t.me/TheVenomXD long msg_id
        self.chat_instance = chat_instance  # t.me/TheVenomXD long data
        self.game_short_name = game_short_name  # t.me/TheVenomXD flags.1?string 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateInlineBotCallbackQuery":
        
        flags = TLObject.read(b)
        
        octra_user_id = TLObject.read(b)
        
        chat_instance = TLObject.read(b)
        
        game_short_name = String.read(b) if flags & (1 << 1) else None
        return UpdateInlineBotCallbackQuery(flags=flags, octra_user_id=octra_user_id, chat_instance=chat_instance, game_short_name=game_short_name)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.octra_user_id.write())
        
        b.write(self.chat_instance.write())
        
        if self.game_short_name is not None:
            b.write(String(self.game_short_name))
        
        return b.getvalue()
