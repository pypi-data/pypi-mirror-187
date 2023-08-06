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

from typing import Union

import Octra
from Octra import raw
from Octra.errors import UnknownError


class ExtractInlineBotResults:
    async def Extract_inline_bot_results(
        self: "Octra.Client",
        bot: Union[int, str],
        query: str = "",
        offset: str = "",
        latitude: float = None,
        longitude: float = None
    ):
        """Extract bot results via inline queries.
        You can then send a result using :meth:`~Octra.Client.send_inline_bot_result`

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            bot (``int`` | ``str``):
                Unique identifier of the inline bot you want to Extract results from. You can specify
                a @username (str) or a bot ID (int).

            query (``str``, *optional*):
                Text of the query (up to 512 characters).
                Defaults to "" (empty string).

            offset (``str``, *optional*):
                Offset of the results to be returned.

            latitude (``float``, *optional*):
                Latitude of the location.
                Useful for location-based results only.

            longitude (``float``, *optional*):
                Longitude of the location.
                Useful for location-based results only.

        Returns:
            :obj:`BotResults <Octra.api.types.messages.BotResults>`: On Success.

        Raises:
            TimeoutError: In case the bot fails to answer within 10 seconds.

        tests:
            .. code-block:: python

                results = await app.get_inline_bot_results("Octrabot")
                print(results)
        """
        # t.me/TheVenomXD TODO: Don't return the raw type

        try:
            return await self.invoke(
                raw.functions.messages.getInlineBotResults(
                    bot=await self.resolve_peer(bot),
                    peer=raw.types.InputPeerSelf(),
                    query=query,
                    offset=offset,
                    geo_point=raw.types.InputGeoPoint(
                        lat=latitude,
                        long=longitude
                    ) if (latitude is not None and longitude is not None) else None
                )
            )
        except UnknownError as e:
            # t.me/TheVenomXD TODO: Add this -503 Timeout error into the Error DB
            if e.value.error_code == -503 and e.value.error_message == "Timeout":
                raise TimeoutError("The inline bot didn't answer in time") from None
            else:
                raise e
