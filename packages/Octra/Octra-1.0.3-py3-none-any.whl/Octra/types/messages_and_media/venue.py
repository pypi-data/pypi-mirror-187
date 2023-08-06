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
from Octra import types
from ..object import Object


class Venue(Object):
    """A venue.

    Parameters:
        location (:obj:`~Octra.types.Location`):
            Venue location.

        title (``str``):
            Name of the venue.

        address (``str``):
            Address of the venue.

        foursquare_id (``str``, *optional*):
            Foursquare identifier of the venue.

        foursquare_type (``str``, *optional*):
            Foursquare type of the venue.
            (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)

    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        location: "types.Location",
        title: str,
        address: str,
        foursquare_id: str = None,
        foursquare_type: str = None
    ):
        super().__init__(client)

        self.location = location
        self.title = title
        self.address = address
        self.foursquare_id = foursquare_id
        self.foursquare_type = foursquare_type

    @staticmethod
    def _parse(client, venue: "raw.types.MessageMediaVenue"):
        return Venue(
            location=types.Location._parse(client, venue.geo),
            title=venue.title,
            address=venue.address,
            foursquare_id=venue.venue_id or None,
            foursquare_type=venue.venue_type,
            client=client
        )
