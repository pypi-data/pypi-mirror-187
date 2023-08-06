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

from typing import Union, List

import Octra
from Octra import raw
from Octra import types


class ExtractGameHighScores:
    async def Extract_game_high_scores(
        self: "Octra.Client",
        octra_user_id: Union[int, str],
        chat_id: Union[int, str],
        message_id: int = None
    ) -> List["types.GameHighScore"]:
        """Extract data for high score tables.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            octra_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the tarExtract chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                Required if inline_message_id is not specified.

            message_id (``int``, *optional*):
                Identifier of the sent message.
                Required if inline_message_id is not specified.

        Returns:
            List of :obj:`~Octra.types.GameHighScore`: On success.

        tests:
            .. code-block:: python

                scores = await app.get_game_high_scores(octra_user_id, chat_id, message_id)
                print(scores)
        """
        # t.me/TheVenomXD TODO: inline_message_id

        r = await self.invoke(
            raw.functions.messages.getGameHighScores(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                octra_user_id=await self.resolve_peer(octra_user_id)
            )
        )

        return types.List(types.GameHighScore._parse(self, score, r.users) for score in r.scores)
