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


class CodeSettings(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.CodeSettings`.

    Details:
        - Layer: ``151``
        - ID: ``8A6469C2``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD allow_flashcall <Octra.raw.base.# t.me/TheVenomXD allow_flashcall>`):
            N/A

        current_number (:obj:`true allow_app_hash <Octra.raw.base.true allow_app_hash>`, *optional*):
            N/A

        allow_missed_call (:obj:`true logout_tokens <Octra.raw.base.true logout_tokens>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["flags", "current_number", "allow_missed_call"]

    ID = 0x8a6469c2
    QUALNAME = "types.CodeSettings"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD allow_flashcall", current_number: "raw.base.true allow_app_hash" = None, allow_missed_call: "raw.base.true logout_tokens" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD allow_flashcall
        self.current_number = current_number  # t.me/TheVenomXD flags.1?true allow_app_hash
        self.allow_missed_call = allow_missed_call  # t.me/TheVenomXD flags.5?true logout_tokens

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CodeSettings":
        
        flags = TLObject.read(b)
        
        current_number = True if flags & (1 << 1) else False
        allow_missed_call = True if flags & (1 << 5) else False
        return CodeSettings(flags=flags, current_number=current_number, allow_missed_call=allow_missed_call)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        return b.getvalue()
