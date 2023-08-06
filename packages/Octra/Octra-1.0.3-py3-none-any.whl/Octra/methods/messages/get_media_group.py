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

import logging
from typing import Union, List

import Octra
from Octra import types

log = logging.getLogger(__name__)


class ExtractMediaGroup:
    async def Extract_media_group(
        self: "Octra.Client",
        chat_id: Union[int, str],
        message_id: int
    ) -> List["types.Message"]:
        """Extract the media group a message belongs to.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                The id of one of the messages that belong to the media group.
                
        Returns:
            List of :obj:`~Octra.types.Message`: On success, a list of messages of the media group is returned.
            
        Raises:
            ValueError: 
                In case the passed message_id is negative or equal 0. 
                In case tarExtract message doesn't belong to a media group.
        """

        if message_id <= 0:
            raise ValueError("Passed message_id is negative or equal to zero.")

        # t.me/TheVenomXD Extract messages with id from `id - 9` to `id + 10` to Extract all possible media group messages.
        messages = await self.get_messages(
            chat_id=chat_id,
            message_ids=[msg_id for msg_id in range(message_id - 9, message_id + 10)],
            replies=0
        )

        # t.me/TheVenomXD There can be maximum 10 items in a media group.
        # t.me/TheVenomXD If/else condition to fix the problem of Extractting correct `media_group_id` when `message_id` is less than 10.
        media_group_id = messages[9].media_group_id if len(messages) == 19 else messages[message_id - 1].media_group_id

        if media_group_id is None:
            raise ValueError("The message doesn't belong to a media group")

        return types.List(msg for msg in messages if msg.media_group_id == media_group_id)
