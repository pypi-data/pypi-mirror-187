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


class UpdateBotCallbackQuery(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Update`.

    Details:
        - Layer: ``151``
        - ID: ``B9CFC48D``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD query_id <Octra.raw.base.# t.me/TheVenomXD query_id>`):
            N/A

        octra_user_id (:obj:`long peer <Octra.raw.base.long peer>`):
            N/A

        msg_id (:obj:`int chat_instance <Octra.raw.base.int chat_instance>`):
            N/A

        data (:obj:`bytes game_short_name <Octra.raw.base.bytes game_short_name>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "octra_user_id", "msg_id", "data"]

    ID = 0xb9cfc48d
    QUALNAME = "types.UpdateBotCallbackQuery"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD query_id", octra_user_id: "raw.base.long peer", msg_id: "raw.base.int chat_instance", data: "raw.base.bytes game_short_name" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD query_id
        self.octra_user_id = octra_user_id  # t.me/TheVenomXD long peer
        self.msg_id = msg_id  # t.me/TheVenomXD int chat_instance
        self.data = data  # t.me/TheVenomXD flags.0?bytes game_short_name

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateBotCallbackQuery":
        
        flags = TLObject.read(b)
        
        octra_user_id = TLObject.read(b)
        
        msg_id = TLObject.read(b)
        
        data = Bytes.read(b) if flags & (1 << 0) else None
        return UpdateBotCallbackQuery(flags=flags, octra_user_id=octra_user_id, msg_id=msg_id, data=data)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.octra_user_id.write())
        
        b.write(self.msg_id.write())
        
        if self.data is not None:
            b.write(Bytes(self.data))
        
        return b.getvalue()
