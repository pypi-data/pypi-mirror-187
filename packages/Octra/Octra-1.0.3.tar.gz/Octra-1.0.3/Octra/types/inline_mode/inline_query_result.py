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

from uuid import uuid4

import Octra
from Octra import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~Octra.types.InlineQueryResultCachedAudio`
    - :obj:`~Octra.types.InlineQueryResultCachedDocument`
    - :obj:`~Octra.types.InlineQueryResultCacheAkashimation`
    - :obj:`~Octra.types.InlineQueryResultCachedPhoto`
    - :obj:`~Octra.types.InlineQueryResultCachedSticker`
    - :obj:`~Octra.types.InlineQueryResultCachedVideo`
    - :obj:`~Octra.types.InlineQueryResultCachedVoice`
    - :obj:`~Octra.types.InlineQueryResultArticle`
    - :obj:`~Octra.types.InlineQueryResultAudio`
    - :obj:`~Octra.types.InlineQueryResultContact`
    - :obj:`~Octra.types.InlineQueryResultDocument`
    - :obj:`~Octra.types.InlineQueryResultAnimation`
    - :obj:`~Octra.types.InlineQueryResultLocation`
    - :obj:`~Octra.types.InlineQueryResultPhoto`
    - :obj:`~Octra.types.InlineQueryResultVenue`
    - :obj:`~Octra.types.InlineQueryResultVideo`
    - :obj:`~Octra.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "Octra.Client"):
        pass
