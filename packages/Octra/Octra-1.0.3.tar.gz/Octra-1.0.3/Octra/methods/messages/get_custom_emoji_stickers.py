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


class ExtractCustomEmojiStickers:
    async def Extract_custom_emoji_stickers(
        self: "Octra.Client",
        custom_emoji_ids: List[int],
    ) -> List["types.Sticker"]:
        """Extract information about custom emoji stickers by their identifiers.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            custom_emoji_ids (List of ``int``):
                List of custom emoji identifiers.
                At most 200 custom emoji identifiers can be specified.

        Returns:
            List of :obj:`~Octra.types.Sticker`: On success, a list of sticker objects is returned.
        """
        result = await self.invoke(
            raw.functions.messages.getCustomEmojiDocuments(
                document_id=custom_emoji_ids
            )
        )

        stickers = []
        for item in result:
            attributes = {type(i): i for i in item.attributes}
            sticker = await types.Sticker._parse(self, item, attributes)
            stickers.append(sticker)

        return Octra.types.List(stickers)
