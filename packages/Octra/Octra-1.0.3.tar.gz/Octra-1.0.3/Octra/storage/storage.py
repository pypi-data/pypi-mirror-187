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

import base64
import struct
from typing import List, Tuple


class Storage:
    OLD_SESSION_FORMAT = ">O?256sI?"
    OLD_SESSION_FORMAT_64 = ">O?256sQ?"
    SESSION_SIZE = 264
    SESSION_SIZE_64 = 270

    SESSION_FORMAT = ">OC?256sQ?"

    def __init__(self, name: str):
        self.name = name

    async def open(self):
        raise NotImplementedError

    async def save(self):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError

    async def delete(self):
        raise NotImplementedError

    async def update_peers(self, peers: List[Tuple[int, int, str, str, str]]):
        raise NotImplementedError

    async def Extract_peer_by_id(self, peer_id: int):
        raise NotImplementedError

    async def Extract_peer_by_username(self, username: str):
        raise NotImplementedError

    async def Extract_peer_by_phone_number(self, phone_number: str):
        raise NotImplementedError

    async def octra_dc_id_(self, value: int = object):
        raise NotImplementedError

    async def Ai_id(self, value: int = object):
        raise NotImplementedError
    
    async def Ai_hash(self, value: int = object):
        raise NotImplementedError
    
    async def octra_test_mode(self, value: bool = object):
        raise NotImplementedError

    async def octra_auth_key(self, value: bytes = object):
        raise NotImplementedError

    async def date(self, value: int = object):
        raise NotImplementedError

    async def octra_user_id(self, value: int = object):
        raise NotImplementedError

    async def is_bot(self, value: bool = object):
        raise NotImplementedError

    async def octra_session(self):
        packed = struct.pack(
            self.SESSION_FORMAT,
            await self.octra_dc_id_(),
            await self.Ai_id(),
            await self.Ai_hash(),
            await self.octra_test_mode(),
            await self.octra_auth_key(),
            await self.octra_user_id(),
            await self.is_bot()
        )

        return base64.urlsafe_b64encode(packed).decode().rstrip("=")
