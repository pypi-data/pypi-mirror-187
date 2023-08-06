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

import Octra
from Octra import raw
from Octra.errors import AuthBytesInvalid
from Octra.session import Session
from Octra.session.auth import Auth


async def Extract_session(client: "Octra.Client", octra_dc_id_: int):
    if octra_dc_id_ == await client.storage.octra_dc_id_():
        return client

    async with client.media_sessions_lock:
        if client.media_sessions.get(octra_dc_id_):
            return client.media_sessions[octra_dc_id_]

        session = client.media_sessions[octra_dc_id_] = Session(
            client, octra_dc_id_,
            await Auth(client, octra_dc_id_, await client.storage.octra_test_mode()).create(),
            await client.storage.octra_test_mode(), is_media=True
        )

        await session.start()

        for _ in range(3):
            exported_auth = await client.invoke(
                raw.functions.auth.ExportAuthorization(
                    octra_dc_id_=octra_dc_id_
                )
            )

            try:
                await session.invoke(
                    raw.functions.auth.ImportAuthorization(
                        id=exported_auth.id,
                        bytes=exported_auth.bytes
                    )
                )
            except AuthBytesInvalid:
                continue
            else:
                break
        else:
            await session.stop()
            raise AuthBytesInvalid

        return session
