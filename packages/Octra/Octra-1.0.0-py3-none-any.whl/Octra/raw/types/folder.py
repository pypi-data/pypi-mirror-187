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


class Folder(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Folder`.

    Details:
        - Layer: ``151``
        - ID: ``FF544E65``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD autofill_new_broadcasts <Octra.raw.base.# t.me/TheVenomXD autofill_new_broadcasts>`):
            N/A

        id (:obj:`int title <Octra.raw.base.int title>`):
            N/A

        autofill_public_groups (:obj:`true autofill_new_correspondents <Octra.raw.base.true autofill_new_correspondents>`, *optional*):
            N/A

        photo (:obj:`ChatPhoto  <Octra.raw.base.ChatPhoto >`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "id", "autofill_public_groups", "photo"]

    ID = 0xff544e65
    QUALNAME = "types.Folder"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD autofill_new_broadcasts", id: "raw.base.int title", autofill_public_groups: "raw.base.true autofill_new_correspondents" = None, photo: "raw.base.ChatPhoto " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD autofill_new_broadcasts
        self.id = id  # t.me/TheVenomXD int title
        self.autofill_public_groups = autofill_public_groups  # t.me/TheVenomXD flags.1?true autofill_new_correspondents
        self.photo = photo  # t.me/TheVenomXD flags.3?ChatPhoto 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Folder":
        
        flags = TLObject.read(b)
        
        autofill_public_groups = True if flags & (1 << 1) else False
        id = TLObject.read(b)
        
        photo = TLObject.read(b) if flags & (1 << 3) else None
        
        return Folder(flags=flags, id=id, autofill_public_groups=autofill_public_groups, photo=photo)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.id.write())
        
        if self.photo is not None:
            b.write(self.photo.write())
        
        return b.getvalue()
