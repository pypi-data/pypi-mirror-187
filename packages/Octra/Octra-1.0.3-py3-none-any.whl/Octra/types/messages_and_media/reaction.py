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

from typing import Optional

import Octra
from Octra import raw
from ..object import Object


class Reaction(Object):
    """Contains information about a reaction.

    Parameters:
        emoji (``str``, *optional*):
            Reaction emoji.

        custom_emoji_id (``int``, *optional*):
            Custom emoji id.

        count (``int``, *optional*):
            Reaction count.

        chosen_order (``int``, *optional*):
            Chosen reaction order.
            Available for chosen reactions.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        emoji: Optional[str] = None,
        custom_emoji_id: Optional[int] = None,
        count: Optional[int] = None,
        chosen_order: Optional[int] = None
    ):
        super().__init__(client)

        self.emoji = emoji
        self.custom_emoji_id = custom_emoji_id
        self.count = count
        self.chosen_order = chosen_order

    @staticmethod
    def _parse(
        client: "Octra.Client",
        reaction: "raw.base.Reaction"
    ) -> "Reaction":
        if isinstance(reaction, raw.types.ReactionEmoji):
            return Reaction(
                client=client,
                emoji=reaction.emoticon
            )

        if isinstance(reaction, raw.types.ReactionCustomEmoji):
            return Reaction(
                client=client,
                custom_emoji_id=reaction.document_id
            )

    @staticmethod
    def _parse_count(
        client: "Octra.Client",
        reaction_count: "raw.base.ReactionCount"
    ) -> "Reaction":
        reaction = Reaction._parse(client, reaction_count.reaction)
        reaction.count = reaction_count.count
        reaction.chosen_order = reaction_count.chosen_order

        return reaction
