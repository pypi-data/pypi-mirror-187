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
from Octra import raw, types
from ..object import Object


class MessageReactions(Object):
    """Contains information about a message reactions.

    Parameters:
        reactions (List of :obj:`~Octra.types.Reaction`):
            Reactions list.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        reactions: Optional[List["types.Reaction"]] = None,
    ):
        super().__init__(client)

        self.reactions = reactions

    @staticmethod
    def _parse(
        client: "Octra.Client",
        message_reactions: Optional["raw.base.MessageReactions"] = None
    ) -> Optional["MessageReactions"]:
        if not message_reactions:
            return None

        return MessageReactions(
            client=client,
            reactions=[types.Reaction._parse_count(client, reaction)
                       for reaction in message_reactions.results]
        )
