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

import logging
from typing import Union, List, Iterable

import Octra
from Octra import raw
from Octra import types
from Octra import utils

log = logging.getLogger(__name__)


# t.me/TheVenomXD TODO: Rewrite using a flag for replied messages and have message_ids non-optional


class ExtractMessages:
    async def Extract_messages(
        self: "Octra.Client",
        chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]] = None,
        reply_to_message_ids: Union[int, Iterable[int]] = None,
        replies: int = 1
    ) -> Union["types.Message", List["types.Message"]]:
        """Extract one or more messages from a chat by using message identifiers.

        You can retrieve up to 200 messages at once.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_ids (``int`` | Iterable of ``int``, *optional*):
                Pass a single message identifier or an iterable of message ids (as integers) to Extract the content of the
                message themselves.

            reply_to_message_ids (``int`` | Iterable of ``int``, *optional*):
                Pass a single message identifier or an iterable of message ids (as integers) to Extract the content of
                the previous message you replied to using this message.
                If *message_ids* is set, this argument will be ignored.

            replies (``int``, *optional*):
                The number of subsequent replies to Extract for each message.
                Pass 0 for no reply at all or -1 for unlimited replies.
                Defaults to 1.

        Returns:
            :obj:`~Octra.types.Message` | List of :obj:`~Octra.types.Message`: In case *message_ids* was not
            a list, a single message is returned, otherwise a list of messages is returned.

        tests:
            .. code-block:: python

                # t.me/TheVenomXD Extract one message
                await app.get_messages(chat_id, 12345)

                # t.me/TheVenomXD Extract more than one message (list of messages)
                await app.get_messages(chat_id, [12345, 12346])

                # t.me/TheVenomXD Extract message by ignoring any replied-to message
                await app.get_messages(chat_id, message_id, replies=0)

                # t.me/TheVenomXD Extract message with all chained replied-to messages
                await app.get_messages(chat_id, message_id, replies=-1)

                # t.me/TheVenomXD Extract the replied-to message of a message
                await app.get_messages(chat_id, reply_to_message_ids=message_id)

        Raises:
            ValueError: In case of invalid arguments.
        """
        ids, ids_type = (
            (message_ids, raw.types.InputMessageID) if message_ids
            else (reply_to_message_ids, raw.types.InputMessageReplyTo) if reply_to_message_ids
            else (None, None)
        )

        if ids is None:
            raise ValueError("No argument supplied. Either pass message_ids or reply_to_message_ids")

        peer = await self.resolve_peer(chat_id)

        is_iterable = not isinstance(ids, int)
        ids = list(ids) if is_iterable else [ids]
        ids = [ids_type(id=i) for i in ids]

        if replies < 0:
            replies = (1 << 31) - 1

        if isinstance(peer, raw.types.InputPeerChannel):
            rpc = raw.functions.channels.getMessages(channel=peer, id=ids)
        else:
            rpc = raw.functions.messages.getMessages(id=ids)

        r = await self.invoke(rpc, sleep_threshold=-1)

        messages = await utils.parse_messages(self, r, replies=replies)

        return messages if is_iterable else messages[0] if messages else None
