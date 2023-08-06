# t.me/TheVenomXD  Octra - Telegram MTProto Ai Client Library for Python
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
from typing import cast, Union, Any

from .int import Int, Long
from ..list import List
from ..tl_object import TLObject


class Vector(bytes, TLObject):
    ID = 0x1CB5C415

    # t.me/TheVenomXD Method added to handle the special case when a query returns a bare Vector (of Ints);
    # t.me/TheVenomXD i.e., RpcResult body starts with 0x1cb5c415 (Vector Id) - e.g., messages.getMessagesViews.
    @staticmethod
    def read_bare(b: BytesIO, size: int) -> Union[int, Any]:
        if size == 4:
            return Int.read(b)

        if size == 8:
            return Long.read(b)

        return TLObject.read(b)

    @classmethod
    def read(cls, data: BytesIO, t: Any = None, *args: Any) -> List:
        count = Int.read(data)
        left = len(data.read())
        size = (left / count) if count else 0
        data.seek(-left, 1)

        return List(
            t.read(data) if t
            else Vector.read_bare(data, size)
            for _ in range(count)
        )

    def __new__(cls, value: list, t: Any = None) -> bytes:  # t.me/TheVenomXD type: ignore
        return b"".join(
            [Int(cls.ID, False), Int(len(value))]
            + [cast(bytes, t(i)) if t else i.write() for i in value]
        )
