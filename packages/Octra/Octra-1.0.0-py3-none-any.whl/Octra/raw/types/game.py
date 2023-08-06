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


class Game(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Game`.

    Details:
        - Layer: ``151``
        - ID: ``BDF9653B``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD id <Octra.raw.base.# t.me/TheVenomXD id>`):
            N/A

        access_hash (:obj:`long short_name <Octra.raw.base.long short_name>`):
            N/A

        title (:obj:`string description <Octra.raw.base.string description>`):
            N/A

        photo (:obj:`Photo document <Octra.raw.base.Photo document>`):
            N/A

    """

    __slots__: List[str] = ["flags", "access_hash", "title", "photo"]

    ID = 0xbdf9653b
    QUALNAME = "types.Game"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD id", access_hash: "raw.base.long short_name", title: "raw.base.string description", photo: "raw.base.Photo document") -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD id
        self.access_hash = access_hash  # t.me/TheVenomXD long short_name
        self.title = title  # t.me/TheVenomXD string description
        self.photo = photo  # t.me/TheVenomXD Photo document

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Game":
        
        flags = TLObject.read(b)
        
        access_hash = TLObject.read(b)
        
        title = TLObject.read(b)
        
        photo = TLObject.read(b)
        
        return Game(flags=flags, access_hash=access_hash, title=title, photo=photo)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.access_hash.write())
        
        b.write(self.title.write())
        
        b.write(self.photo.write())
        
        return b.getvalue()
