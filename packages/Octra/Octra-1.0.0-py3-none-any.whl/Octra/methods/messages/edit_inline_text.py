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

from typing import Optional

import Octra
from Octra import raw, enums
from Octra import types
from Octra import utils
from .inline_session import Extract_session


class EditInlineText:
    async def edit_inline_text(
        self: "Octra.Client",
        inline_message_id: str,
        text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        disable_web_page_preview: bool = None,
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> bool:
        """Edit the text of inline messages.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            inline_message_id (``str``):
                Identifier of the inline message.

            text (``str``):
                New text of the message.

            parse_mode (:obj:`~Octra.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes toExtracther.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            reply_markup (:obj:`~Octra.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            ``bool``: On success, True is returned.

        tests:
            .. code-block:: python

                # t.me/TheVenomXD Bots only

                # t.me/TheVenomXD Simple edit text
                await app.edit_inline_text(inline_message_id, "new text")

                # t.me/TheVenomXD Take the same text message, remove the web page preview only
                await app.edit_inline_text(
                    inline_message_id, message.text,
                    disable_web_page_preview=True)
        """

        unpacked = utils.unpack_inline_message_id(inline_message_id)
        octra_dc_id_ = unpacked.octra_dc_id_

        session = await Extract_session(self, octra_dc_id_)

        return await session.invoke(
            raw.functions.messages.EditInlineBotMessage(
                id=unpacked,
                no_webpage=disable_web_page_preview or None,
                reply_markup=await reply_markup.write(self) if reply_markup else None,
                **await self.parser.parse(text, parse_mode)
            ),
            sleep_threshold=self.sleep_threshold
        )
