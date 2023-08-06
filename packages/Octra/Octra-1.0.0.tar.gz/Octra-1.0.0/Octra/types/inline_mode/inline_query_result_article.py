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
from Octra import raw
from Octra import types

from .inline_query_result import InlineQueryResult


class InlineQueryResultArticle(InlineQueryResult):
    """Link to an article or web page.

    Parameters:
        title (``str``):
            Title for the result.

        input_message_content (:obj:`~Octra.types.InputMessageContent`):
            Content of the message to be sent.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        url (``str``, *optional*):
            URL of the result.

        description (``str``, *optional*):
            Short description of the result.

        reply_markup (:obj:`~Octra.types.InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.

        thumb_url (``str``, *optional*):
            Url of the thumbnail for the result.

        thumb_width (``int``, *optional*):
            Thumbnail width.

        thumb_height (``int``, *optional*):
            Thumbnail height
    """

    def __init__(
        self,
        title: str,
        input_message_content: "types.InputMessageContent",
        id: str = None,
        url: str = None,
        description: str = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        thumb_url: str = None,
        thumb_width: int = 0,
        thumb_height: int = 0
    ):
        super().__init__("article", id, input_message_content, reply_markup)

        self.title = title
        self.url = url
        self.description = description
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    async def write(self, client: "Octra.Client"):
        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            send_message=await self.input_message_content.write(client, self.reply_markup),
            title=self.title,
            description=self.description,
            url=self.url,
            thumb=raw.types.InputWebDocument(
                url=self.thumb_url,
                size=0,
                mime_type="image/jpeg",
                attributes=[
                    raw.types.DocumentAttributeImageSize(
                        w=self.thumb_width,
                        h=self.thumb_height
                    )
                ]
            ) if self.thumb_url else None
        )
