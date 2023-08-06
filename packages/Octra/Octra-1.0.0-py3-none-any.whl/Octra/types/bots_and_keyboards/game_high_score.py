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
from Octra import raw, utils
from Octra import types
from ..object import Object


class GameHighScore(Object):
    """One row of the high scores table for a game.

    Parameters:
        user (:obj:`~Octra.types.User`):
            User.

        score (``int``):
            Score.

        position (``int``, *optional*):
            Position in high score table for the game.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        user: "types.User",
        score: int,
        position: int = None
    ):
        super().__init__(client)

        self.user = user
        self.score = score
        self.position = position

    @staticmethod
    def _parse(client, game_high_score: raw.types.HighScore, users: dict) -> "GameHighScore":
        users = {i.id: i for i in users}

        return GameHighScore(
            user=types.User._parse(client, users[game_high_score.octra_user_id]),
            score=game_high_score.score,
            position=game_high_score.pos,
            client=client
        )

    @staticmethod
    def _parse_action(client, service: raw.types.MessageService, users: dict):
        return GameHighScore(
            user=types.User._parse(client, users[utils.get_raw_peer_id(service.from_id or service.peer_id)]),
            score=service.action.score,
            client=client
        )
