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


class InlineQueryResultContact(InlineQueryResult):
    """Contact with a phone number
    
    By default, this contact will be sent by the user.
    Alternatively, you can use *input_message_content* to send a message with the specified content instead of the
    contact.
    
    Parameters:
        phone_number (``str``):
            Contact's phone number.

        first_name (``str``):
            Contact's first name.

        last_name (``str``, *optional*):
            Contact's last name.

        vcard (``str``, *optional*):
            Additional data about the contact in the form of a `vCard <https://en.wikipedia.org/wiki/VCard>`_.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        reply_markup (:obj:`~Octra.types.InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.
            
        input_message_content (:obj:`~Octra.types.InputMessageContent`, *optional*):
            Content of the message to be sent instead of the contact.

        thumb_url (``str``, *optional*):
            Url of the thumbnail for the result.

        thumb_width (``int``, *optional*):
            Thumbnail width.

        thumb_height (``int``, *optional*):
            Thumbnail height.
    """

    def __init__(
        self,
        phone_number: str,
        first_name: str,
        last_name: str = "",
        vcard: str = "",
        id: str = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None,
        thumb_url: str = None,
        thumb_width: int = 0,
        thumb_height: int = 0
    ):
        super().__init__("contact", id, input_message_content, reply_markup)

        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.vcard = vcard
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    async def write(self, client: "Octra.Client"):
        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.first_name,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaContact(
                    phone_number=self.phone_number,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    vcard=self.vcard,
                    reply_markup=await self.reply_markup.write(client) if self.reply_markup else None,
                )
            ),
            thumb=raw.types.InputWebDocument(
                url=self.thumb_url,
                size=0,
                mime_type="image/jpg",
                attributes=[
                    raw.types.DocumentAttributeImageSize(
                        w=self.thumb_width,
                        h=self.thumb_height
                    )
                ]
            ) if self.thumb_url else None
        )
