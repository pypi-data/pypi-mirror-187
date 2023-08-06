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


class UploadProfilePhoto(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``89F30F69``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD fallback <Octra.raw.base.# t.me/TheVenomXD fallback>`):
            N/A

        file (:obj:`InputFile video <Octra.raw.base.InputFile video>`, *optional*):
            N/A

        video_start_ts (:obj:`double  <Octra.raw.base.double >`, *optional*):
            N/A

    Returns:
        :obj:`photos.Photo <Octra.raw.base.photos.Photo>`
    """

    __slots__: List[str] = ["flags", "file", "video_start_ts"]

    ID = 0x89f30f69
    QUALNAME = "functions.photos.UploadProfilePhoto"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD fallback", file: "raw.base.InputFile video" = None, video_start_ts: "raw.base.double " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD fallback
        self.file = file  # t.me/TheVenomXD flags.0?InputFile video
        self.video_start_ts = video_start_ts  # t.me/TheVenomXD flags.2?double 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UploadProfilePhoto":
        
        flags = TLObject.read(b)
        
        file = TLObject.read(b) if flags & (1 << 0) else None
        
        video_start_ts = Double.read(b) if flags & (1 << 2) else None
        return UploadProfilePhoto(flags=flags, file=file, video_start_ts=video_start_ts)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.file is not None:
            b.write(self.file.write())
        
        if self.video_start_ts is not None:
            b.write(Double(self.video_start_ts))
        
        return b.getvalue()
