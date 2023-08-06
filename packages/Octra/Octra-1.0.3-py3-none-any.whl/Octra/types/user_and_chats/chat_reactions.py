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

from typing import Optional, List

import Octra
from Octra import raw, types
from ..object import Object


class ChatReactions(Object):
    """A chat reactions

    Parameters:
        all_are_enabled (``bool``, *optional*)

        allow_custom_emoji (``bool``, *optional*):
            Whether custom emoji are allowed or not.

        reactions (List of :obj:`~Octra.types.Reaction`, *optional*):
            Reactions available.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        all_are_enabled: Optional[bool] = None,
        allow_custom_emoji: Optional[bool] = None,
        reactions: Optional[List["types.Reaction"]] = None,
    ):
        super().__init__(client)

        self.all_are_enabled = all_are_enabled
        self.allow_custom_emoji = allow_custom_emoji
        self.reactions = reactions

    @staticmethod
    def _parse(client, chat_reactions: "raw.base.ChatReactions") -> Optional["ChatReactions"]:
        if isinstance(chat_reactions, raw.types.ChatReactionsAll):
            return ChatReactions(
                client=client,
                all_are_enabled=True,
                allow_custom_emoji=chat_reactions.allow_custom
            )

        if isinstance(chat_reactions, raw.types.ChatReactionsSome):
            return ChatReactions(
                client=client,
                reactions=[types.Reaction._parse(client, reaction)
                           for reaction in chat_reactions.reactions]
            )

        return None
