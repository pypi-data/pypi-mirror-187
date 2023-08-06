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

import Octra
from Octra import raw, types
from .inline_query_result import InlineQueryResult


class InlineQueryResultVenue(InlineQueryResult):
    """A venue.

    By default, the venue will be sent by the user. Alternatively, you can use *input_message_content* to send a message
    with the specified content instead of the venue.

    Parameters:
        title (``str``):
            Title for the result.

        address (``str``):
            Address of the venue.

        latitude (``float``):
            Location latitude in degrees.

        longitude (``float``):
            Location longitude in degrees.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        foursquare_id (``str``, *optional*):
            Foursquare identifier of the venue if known.

        foursquare_type (``str``, *optional*):
            Foursquare type of the venue, if known.

        google_place_id (``str``, *optional*):
            Google Places identifier of the venue.

        google_place_type (``str``, *optional*):
            Google Places type of the venue.

        reply_markup (:obj:`~Octra.types.InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.

        input_message_content (:obj:`~Octra.types.InputMessageContent`):
            Content of the message to be sent instead of the file.

        thumb_url (``str``, *optional*):
            Url of the thumbnail for the result.

        thumb_width (``int``, *optional*):
            Thumbnail width.

        thumb_height (``int``, *optional*):
            Thumbnail height.
    """

    def __init__(
        self,
        title: str,
        address: str,
        latitude: float,
        longitude: float,
        id: str = None,
        foursquare_id: str = None,
        foursquare_type: str = None,
        google_place_id: str = None,
        google_place_type: str = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None,
        thumb_url: str = None,
        thumb_width: int = 0,
        thumb_height: int = 0
    ):
        super().__init__("venue", id, input_message_content, reply_markup)

        self.title = title
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.foursquare_id = foursquare_id
        self.foursquare_type = foursquare_type
        self.google_place_id = google_place_id
        self.google_place_type = google_place_type
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    async def write(self, client: "Octra.Client"):
        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.title,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaVenue(
                    geo_point=raw.types.InputGeoPoint(
                        lat=self.latitude,
                        long=self.longitude
                    ),
                    title=self.title,
                    address=self.address,
                    provider=(
                        "foursquare" if self.foursquare_id or self.foursquare_type
                        else "google" if self.google_place_id or self.google_place_type
                        else ""
                    ),
                    venue_id=self.foursquare_id or self.google_place_id or "",
                    venue_type=self.foursquare_type or self.google_place_type or "",
                    reply_markup=await self.reply_markup.write(client) if self.reply_markup else None
                )
            )
        )
