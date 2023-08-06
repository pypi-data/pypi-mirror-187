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

from typing import Optional, List

import Octra
from Octra import raw, types, utils, enums
from .inline_query_result import InlineQueryResult
from ...file_id import FileId


class InlineQueryResultCachedAudio(InlineQueryResult):
    """A link to an MP3 audio file stored on the Telegram servers

    By default, this audio file will be sent by the user. Alternatively, you can use *input_message_content* to send a
    message with the specified content instead of the audio.

    Parameters:
        audio_file_id (``str``):
            A valid file identifier for the audio file.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        caption (``str``, *optional*):
            Caption of the photo to be sent, 0-1024 characters.

        parse_mode (:obj:`~Octra.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes toExtracther.

        caption_entities (List of :obj:`~Octra.types.MessageEntity`):
            List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        reply_markup (:obj:`~Octra.types.InlineKeyboardMarkup`, *optional*):
            An InlineKeyboardMarkup object.

        input_message_content (:obj:`~Octra.types.InputMessageContent`):
            Content of the message to be sent instead of the photo.
    """

    def __init__(
        self,
        audio_file_id: str,
        id: str = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None
    ):
        super().__init__("audio", id, input_message_content, reply_markup)

        self.audio_file_id = audio_file_id
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    async def write(self, client: "Octra.Client"):
        message, entities = (await utils.parse_text_entities(
            client, self.caption, self.parse_mode, self.caption_entities
        )).values()

        file_id = FileId.decode(self.audio_file_id)

        return raw.types.InputBotInlineResultDocument(
            id=self.id,
            type=self.type,
            document=raw.types.InputDocument(
                id=file_id.media_id,
                access_hash=file_id.access_hash,
                file_reference=file_id.file_reference,
            ),
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=await self.reply_markup.write(client) if self.reply_markup else None,
                    message=message,
                    entities=entities
                )
            )
        )
