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


class UserProfilePhoto(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.UserProfilePhoto`.

    Details:
        - Layer: ``151``
        - ID: ``82D1F706``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD has_video <Octra.raw.base.# t.me/TheVenomXD has_video>`):
            N/A

        personal (:obj:`true photo_id <Octra.raw.base.true photo_id>`, *optional*):
            N/A

        stripped_thumb (:obj:`bytes octra_dc_id_ <Octra.raw.base.bytes octra_dc_id_>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "personal", "stripped_thumb"]

    ID = 0x82d1f706
    QUALNAME = "types.UserProfilePhoto"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD has_video", personal: "raw.base.true photo_id" = None, stripped_thumb: "raw.base.bytes octra_dc_id_" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD has_video
        self.personal = personal  # t.me/TheVenomXD flags.2?true photo_id
        self.stripped_thumb = stripped_thumb  # t.me/TheVenomXD flags.1?bytes octra_dc_id_

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UserProfilePhoto":
        
        flags = TLObject.read(b)
        
        personal = True if flags & (1 << 2) else False
        stripped_thumb = Bytes.read(b) if flags & (1 << 1) else None
        return UserProfilePhoto(flags=flags, personal=personal, stripped_thumb=stripped_thumb)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        if self.stripped_thumb is not None:
            b.write(Bytes(self.stripped_thumb))
        
        return b.getvalue()
