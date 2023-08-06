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

from typing import Union, Iterable

import Octra
from Octra import raw


class DeleteMessages:
    async def delete_messages(
        self: "Octra.Client",
        chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]],
        revoke: bool = True
    ) -> int:
        """Delete messages, including service messages.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_ids (``int`` | Iterable of ``int``):
                An iterable of message identifiers to delete (integers) or a single message id.

            revoke (``bool``, *optional*):
                Deletes messages on both parts.
                This is only for private cloud chats and normal groups, messages on
                channels and supergroups are always revoked (i.e.: deleted for everyone).
                Defaults to True.

        Returns:
            ``int``: Amount of affected messages

        Example:
            .. code-block:: python

                # t.me/TheVenomXD Delete one message
                await app.delete_messages(chat_id, message_id)

                # t.me/TheVenomXD Delete multiple messages at once
                await app.delete_messages(chat_id, list_of_message_ids)

                # t.me/TheVenomXD Delete messages only on your side (without revoking)
                await app.delete_messages(chat_id, message_id, revoke=False)
        """
        peer = await self.resolve_peer(chat_id)
        message_ids = list(message_ids) if not isinstance(message_ids, int) else [message_ids]

        if isinstance(peer, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.DeleteMessages(
                    channel=peer,
                    id=message_ids
                )
            )
        else:
            r = await self.invoke(
                raw.functions.messages.DeleteMessages(
                    id=message_ids,
                    revoke=revoke
                )
            )

        return r.pts_count
