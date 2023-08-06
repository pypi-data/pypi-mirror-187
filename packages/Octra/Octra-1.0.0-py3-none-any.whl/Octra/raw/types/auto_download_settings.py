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


class AutoDownloadSettings(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.AutoDownloadSettings`.

    Details:
        - Layer: ``151``
        - ID: ``8EFAB953``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD disabled <Octra.raw.base.# t.me/TheVenomXD disabled>`):
            N/A

        video_size_max (:obj:`long file_size_max <Octra.raw.base.long file_size_max>`):
            N/A

        video_upload_maxbitrate (:obj:`int  <Octra.raw.base.int >`):
            N/A

        video_preload_large (:obj:`true audio_preload_next <Octra.raw.base.true audio_preload_next>`, *optional*):
            N/A

        phonecalls_less_data (:obj:`true photo_size_max <Octra.raw.base.true photo_size_max>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "video_size_max", "video_upload_maxbitrate", "video_preload_large", "phonecalls_less_data"]

    ID = 0x8efab953
    QUALNAME = "types.AutoDownloadSettings"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD disabled", video_size_max: "raw.base.long file_size_max", video_upload_maxbitrate: "raw.base.int ", video_preload_large: "raw.base.true audio_preload_next" = None, phonecalls_less_data: "raw.base.true photo_size_max" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD disabled
        self.video_size_max = video_size_max  # t.me/TheVenomXD long file_size_max
        self.video_upload_maxbitrate = video_upload_maxbitrate  # t.me/TheVenomXD int 
        self.video_preload_large = video_preload_large  # t.me/TheVenomXD flags.1?true audio_preload_next
        self.phonecalls_less_data = phonecalls_less_data  # t.me/TheVenomXD flags.3?true photo_size_max

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AutoDownloadSettings":
        
        flags = TLObject.read(b)
        
        video_preload_large = True if flags & (1 << 1) else False
        phonecalls_less_data = True if flags & (1 << 3) else False
        video_size_max = TLObject.read(b)
        
        video_upload_maxbitrate = TLObject.read(b)
        
        return AutoDownloadSettings(flags=flags, video_size_max=video_size_max, video_upload_maxbitrate=video_upload_maxbitrate, video_preload_large=video_preload_large, phonecalls_less_data=phonecalls_less_data)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.video_size_max.write())
        
        b.write(self.video_upload_maxbitrate.write())
        
        return b.getvalue()
