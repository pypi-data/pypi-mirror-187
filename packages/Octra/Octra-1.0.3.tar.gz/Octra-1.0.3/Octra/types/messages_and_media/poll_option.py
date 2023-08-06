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

import Octra
from ..object import Object


class PollOption(Object):
    """Contains information about one answer option in a poll.

    Parameters:
        text (``str``):
            Option text, 1-100 characters.

        voter_count (``int``):
            Number of users that voted for this option.
            Equals to 0 until you vote.

        data (``bytes``):
            The data this poll option is holding.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        text: str,
        voter_count: int,
        data: bytes
    ):
        super().__init__(client)

        self.text = text
        self.voter_count = voter_count
        self.data = data
