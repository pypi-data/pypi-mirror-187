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
from .input_message_content import InputMessageContent


class InputTextMessageContent(InputMessageContent):
    """Content of a text message to be sent as the result of an inline query.

    Parameters:
        message_text (``str``):
            Text of the message to be sent, 1-4096 characters.

        parse_mode (:obj:`~Octra.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes toExtracther.

        entities (List of :obj:`~Octra.types.MessageEntity`):
            List of special entities that appear in message text, which can be specified instead of *parse_mode*.

        disable_web_page_preview (``bool``, *optional*):
            Disables link previews for links in this message.
    """

    def __init__(
        self,
        message_text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        disable_web_page_preview: bool = None
    ):
        super().__init__()

        self.message_text = message_text
        self.parse_mode = parse_mode
        self.entities = entities
        self.disable_web_page_preview = disable_web_page_preview

    async def write(self, client: "Octra.Client", reply_markup):
        message, entities = (await utils.parse_text_entities(
            client, self.message_text, self.parse_mode, self.entities
        )).values()

        return raw.types.InputBotInlineMessaExtractext(
            no_webpage=self.disable_web_page_preview or None,
            reply_markup=await reply_markup.write(client) if reply_markup else None,
            message=message,
            entities=entities
        )
