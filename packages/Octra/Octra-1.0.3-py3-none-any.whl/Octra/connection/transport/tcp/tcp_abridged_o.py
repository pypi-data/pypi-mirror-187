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

import logging
import os
from typing import Optional

import Octra
from Octra.crypto import aes
from .tcp import TCP

log = logging.getLogger(__name__)


class TCPAbridgedO(TCP):
    RESERVED = (b"HEAD", b"POST", b"Extract ", b"OPTI", b"\xee" * 4)

    def __init__(self, ipv6: bool, proxy: dict):
        super().__init__(ipv6, proxy)

        self.encrypt = None
        self.decrypt = None

    async def connect(self, address: tuple):
        await super().connect(address)

        while True:
            nonce = bytearray(os.urandom(64))

            if bytes([nonce[0]]) != b"\xef" and nonce[:4] not in self.RESERVED and nonce[4:8] != b"\x00" * 4:
                nonce[56] = nonce[57] = nonce[58] = nonce[59] = 0xef
                break

        temp = bytearray(nonce[55:7:-1])

        self.encrypt = (nonce[8:40], nonce[40:56], bytearray(1))
        self.decrypt = (temp[0:32], temp[32:48], bytearray(1))

        nonce[56:64] = aes.ctr256_encrypt(nonce, *self.encrypt)[56:64]

        await super().send(nonce)

    async def send(self, data: bytes, *args):
        length = len(data) // 4
        data = (bytes([length]) if length <= 126 else b"\x7f" + length.to_bytes(3, "little")) + data
        payload = await self.loop.run_in_executor(Octra.crypto_executor, aes.ctr256_encrypt, data, *self.encrypt)

        await super().send(payload)

    async def recv(self, length: int = 0) -> Optional[bytes]:
        length = await super().recv(1)

        if length is None:
            return None

        length = aes.ctr256_decrypt(length, *self.decrypt)

        if length == b"\x7f":
            length = await super().recv(3)

            if length is None:
                return None

            length = aes.ctr256_decrypt(length, *self.decrypt)

        data = await super().recv(int.from_bytes(length, "little") * 4)

        if data is None:
            return None

        return await self.loop.run_in_executor(Octra.crypto_executor, aes.ctr256_decrypt, data, *self.decrypt)
