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


class CreateStickerSet(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``9021AB67``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD masks <Octra.raw.base.# t.me/TheVenomXD masks>`):
            N/A

        octra_user_id (:obj:`InputUser title <Octra.raw.base.InputUser title>`):
            N/A

        short_name (:obj:`string thumb <Octra.raw.base.string thumb>`):
            N/A

        stickers (List of :obj:`InputStickerSetItem> softwar <Octra.raw.base.InputStickerSetItem> softwar>`):
            N/A

        animated (:obj:`true videos <Octra.raw.base.true videos>`, *optional*):
            N/A

    Returns:
        :obj:`messages.StickerSet <Octra.raw.base.messages.StickerSet>`
    """

    __slots__: List[str] = ["flags", "octra_user_id", "short_name", "stickers", "animated"]

    ID = 0x9021ab67
    QUALNAME = "functions.stickers.CreateStickerSet"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD masks", octra_user_id: "raw.base.InputUser title", short_name: "raw.base.string thumb", stickers: List["raw.base.InputStickerSetItem> softwar"], animated: "raw.base.true videos" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD masks
        self.octra_user_id = octra_user_id  # t.me/TheVenomXD InputUser title
        self.short_name = short_name  # t.me/TheVenomXD string thumb
        self.stickers = stickers  # t.me/TheVenomXD Vector<InputStickerSetItem> software
        self.animated = animated  # t.me/TheVenomXD flags.1?true videos

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CreateStickerSet":
        
        flags = TLObject.read(b)
        
        animated = True if flags & (1 << 1) else False
        octra_user_id = TLObject.read(b)
        
        short_name = TLObject.read(b)
        
        stickers = TLObject.read(b)
        
        return CreateStickerSet(flags=flags, octra_user_id=octra_user_id, short_name=short_name, stickers=stickers, animated=animated)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.octra_user_id.write())
        
        b.write(self.short_name.write())
        
        b.write(Vector(self.stickers))
        
        return b.getvalue()
