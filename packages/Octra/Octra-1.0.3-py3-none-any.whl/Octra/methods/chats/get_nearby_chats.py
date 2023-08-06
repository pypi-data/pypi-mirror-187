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

from typing import List

import Octra
from Octra import raw
from Octra import types
from Octra import utils


class ExtractNearbyChats:
    async def Extract_nearby_chats(
        self: "Octra.Client",
        latitude: float,
        longitude: float
    ) -> List["types.Chat"]:
        """Extract nearby chats.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            latitude (``float``):
                Latitude of the location.

            longitude (``float``):
                Longitude of the location.

        Returns:
            List of :obj:`~Octra.types.Chat`: On success, a list of nearby chats is returned.

        Example:
            .. code-block:: python

                chats = await app.get_nearby_chats(latitude, longitude)
                print(chats)
        """

        r = await self.invoke(
            raw.functions.contacts.getLocated(
                geo_point=raw.types.InputGeoPoint(
                    lat=latitude,
                    long=longitude
                )
            )
        )

        if not r.updates:
            return []

        chats = types.List([types.Chat._parse_chat(self, chat) for chat in r.chats])
        peers = r.updates[0].peers

        for peer in peers:
            if isinstance(peer.peer, raw.types.PeerChannel):
                chat_id = utils.get_channel_id(peer.peer.channel_id)

                for chat in chats:
                    if chat.id == chat_id:
                        chat.distance = peer.distance
                        break

        return chats
