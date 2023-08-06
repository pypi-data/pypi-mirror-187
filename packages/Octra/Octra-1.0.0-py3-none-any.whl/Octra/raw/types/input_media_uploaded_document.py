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


class InputMediaUploadedDocument(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.InputMedia`.

    Details:
        - Layer: ``151``
        - ID: ``5B38C6C1``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD nosound_video <Octra.raw.base.# t.me/TheVenomXD nosound_video>`):
            N/A

        file (:obj:`InputFile thumb <Octra.raw.base.InputFile thumb>`):
            N/A

        mime_type (:obj:`string attributes <Octra.raw.base.string attributes>`):
            N/A

        force_file (:obj:`true spoiler <Octra.raw.base.true spoiler>`, *optional*):
            N/A

        stickers (List of :obj:`InputDocument> ttl_second <Octra.raw.base.InputDocument> ttl_second>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "file", "mime_type", "force_file", "stickers"]

    ID = 0x5b38c6c1
    QUALNAME = "types.InputMediaUploadedDocument"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD nosound_video", file: "raw.base.InputFile thumb", mime_type: "raw.base.string attributes", force_file: "raw.base.true spoiler" = None, stickers: Optional[List["raw.base.InputDocument> ttl_second"]] = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD nosound_video
        self.file = file  # t.me/TheVenomXD InputFile thumb
        self.mime_type = mime_type  # t.me/TheVenomXD string attributes
        self.force_file = force_file  # t.me/TheVenomXD flags.4?true spoiler
        self.stickers = stickers  # t.me/TheVenomXD flags.0?Vector<InputDocument> ttl_seconds

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputMediaUploadedDocument":
        
        flags = TLObject.read(b)
        
        force_file = True if flags & (1 << 4) else False
        file = TLObject.read(b)
        
        mime_type = TLObject.read(b)
        
        stickers = TLObject.read(b) if flags & (1 << 0) else []
        
        return InputMediaUploadedDocument(flags=flags, file=file, mime_type=mime_type, force_file=force_file, stickers=stickers)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.file.write())
        
        b.write(self.mime_type.write())
        
        if self.stickers is not None:
            b.write(Vector(self.stickers))
        
        return b.getvalue()
