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
from Octra import raw

from ..object import Object


class ForceReply(Object):
    """Object used to force clients to show a reply interface.

    Upon receiving a message with this object, Telegram clients will display a reply interface to the user.

    This acts as if the user has selected the bot's message and tapped "Reply".
    This can be extremely useful if you want to create user-friendly step-by-step interfaces without having to
    sacrifice privacy mode.

    Parameters:
        selective (``bool``, *optional*):
            Use this parameter if you want to force reply from specific users only. TarExtracts:
            1) users that are @mentioned in the text of the Message object;
            2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.

        placeholder (``str``, *optional*):
            The placeholder to be shown in the input field when the reply is active; 1-64 characters.
    """

    def __init__(
        self,
        selective: bool = None,
        placeholder: str = None
    ):
        super().__init__()

        self.selective = selective
        self.placeholder = placeholder

    @staticmethod
    def read(b):
        return ForceReply(
            selective=b.selective,
            placeholder=b.placeholder
        )

    async def write(self, _: "Octra.Client"):
        return raw.types.ReplyKeyboardForceReply(
            single_use=True,
            selective=self.selective or None,
            placeholder=self.placeholder or None
        )
