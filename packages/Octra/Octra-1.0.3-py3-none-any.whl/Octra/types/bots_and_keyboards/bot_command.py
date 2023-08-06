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

from Octra import raw

from ..object import Object


class BotCommand(Object):
    """A bot command with the standard slash "/" prefix.

    Parameters:
        command (``str``):
            Text of the command; 1-32 characters.
            Can contain only lowercase English letters, digits and underscores.

        description (``str``):
            Description of the command; 1-256 characters.
    """

    def __init__(self, command: str, description: str):
        super().__init__()

        self.command = command
        self.description = description

    def write(self) -> "raw.types.BotCommand":
        return raw.types.BotCommand(
            command=self.command,
            description=self.description,
        )

    @staticmethod
    def read(c: "raw.types.BotCommand") -> "BotCommand":
        return BotCommand(
            command=c.command,
            description=c.description
        )
