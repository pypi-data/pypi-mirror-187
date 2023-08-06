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

from typing import Union, List

import Octra
from Octra import raw
from Octra import types


class VotePoll:
    async def vote_poll(
        self: "Octra.Client",
        chat_id: Union[int, str],
        message_id: id,
        options: Union[int, List[int]]
    ) -> "types.Poll":
        """Vote a poll.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Identifier of the original message with the poll.

            options (``Int`` | List of ``int``):
                Index or list of indexes (for multiple answers) of the poll option(s) you want to vote for (0 to 9).

        Returns:
            :obj:`~Octra.types.Poll` - On success, the poll with the chosen option is returned.

        Example:
            .. code-block:: python

                await app.vote_poll(chat_id, message_id, 6)
        """

        poll = (await self.get_messages(chat_id, message_id)).poll
        options = [options] if not isinstance(options, list) else options

        r = await self.invoke(
            raw.functions.messages.SendVote(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                options=[poll.options[option].data for option in options]
            )
        )

        return types.Poll._parse(self, r.updates[0])
