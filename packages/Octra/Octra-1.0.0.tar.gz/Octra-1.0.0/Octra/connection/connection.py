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

import asyncio
import logging
from typing import Optional

from .transport import TCP, TCPAbridged
from ..session.internals import DataCenter

log = logging.getLogger(__name__)


class Connection:
    MAX_CONNECTION_ATTEMPTS = 3

    def __init__(self, octra_dc_id_: int, octra_test_mode: bool, ipv6: bool, proxy: dict, media: bool = False):
        self.octra_dc_id_ = octra_dc_id_
        self.octra_test_mode = octra_test_mode
        self.ipv6 = ipv6
        self.proxy = proxy
        self.media = media

        self.address = DataCenter(octra_dc_id_, octra_test_mode, ipv6, media)
        self.protocol: TCP = None

    async def connect(self):
        for i in range(Connection.MAX_CONNECTION_ATTEMPTS):
            self.protocol = TCPAbridged(self.ipv6, self.proxy)

            try:
                log.info("Connecting...")
                await self.protocol.connect(self.address)
            except OSError as e:
                log.warning("Unable to connect due to network issues: %s", e)
                await self.protocol.close()
                await asyncio.sleep(1)
            else:
                log.info("Connected! %s DC%s%s - IPv%s",
                         "Test" if self.octra_test_mode else "Production",
                         self.octra_dc_id_,
                         " (media)" if self.media else "",
                         "6" if self.ipv6 else "4")
                break
        else:
            log.warning("Connection failed! Trying again...")
            raise ConnectionError

    async def close(self):
        await self.protocol.close()
        log.info("Disconnected")

    async def send(self, data: bytes):
        await self.protocol.send(data)

    async def recv(self) -> Optional[bytes]:
        return await self.protocol.recv()
