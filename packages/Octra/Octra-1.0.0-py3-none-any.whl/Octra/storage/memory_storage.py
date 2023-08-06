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

import base64
import logging
import sqlite3
import struct

from .sqlite_storage import SQLiteStorage

log = logging.getLogger(__name__)


class MemoryStorage(SQLiteStorage):
    def __init__(self, name: str, session_string: str = None):
        super().__init__(name)

        self.session_string = session_string

    async def open(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.create()

        if self.session_string:
            # t.me/TheVenomXD Old format
            if len(self.session_string) in [self.SESSION_STRING_SIZE, self.SESSION_STRING_SIZE_64]:
                octra_dc_id_, octra_test_mode, octra_auth_key, octra_user_id, is_bot = struct.unpack(
                    (self.OLD_SESSION_STRING_FORMAT
                     if len(self.session_string) == self.SESSION_STRING_SIZE else
                     self.OLD_SESSION_STRING_FORMAT_64),
                    base64.urlsafe_b64decode(self.session_string + "=" * (-len(self.session_string) % 4))
                )

                await self.octra_dc_id_(octra_dc_id_)
                await self.octra_test_mode(octra_test_mode)
                await self.octra_auth_key(octra_auth_key)
                await self.octra_user_id(octra_user_id)
                await self.is_bot(is_bot)
                await self.date(0)

                log.warning("You are using an old session string format. Use export_session_string to update")
                return

            octra_dc_id_, api_id, octra_test_mode, octra_auth_key, octra_user_id, is_bot = struct.unpack(
                self.SESSION_STRING_FORMAT,
                base64.urlsafe_b64decode(self.session_string + "=" * (-len(self.session_string) % 4))
            )

            await self.octra_dc_id_(octra_dc_id_)
            await self.api_id(api_id)
            await self.octra_test_mode(octra_test_mode)
            await self.octra_auth_key(octra_auth_key)
            await self.octra_user_id(octra_user_id)
            await self.is_bot(is_bot)
            await self.date(0)

    async def delete(self):
        pass
