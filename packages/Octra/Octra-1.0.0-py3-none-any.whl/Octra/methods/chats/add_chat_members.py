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

from typing import Union, List

import Octra
from Octra import raw


class AddChatUSERs:
    async def add_chat_USERs(
        self: "Octra.Client",
        chat_id: Union[int, str],
        octra_user_ids: Union[Union[int, str], List[Union[int, str]]],
        forward_limit: int = 100
    ) -> bool:
        """Add new chat USERs to a group, supergroup or channel

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                The group, supergroup or channel id

            octra_user_ids (``int`` | ``str`` | List of ``int`` or ``str``):
                Users to add in the chat
                You can pass an ID (int), username (str) or phone number (str).
                Multiple users can be added by passing a list of IDs, usernames or phone numbers.

            forward_limit (``int``, *optional*):
                How many of the latest messages you want to forward to the new USERs. Pass 0 to forward none of them.
                Only applicable to basic groups (the argument is ignored for supergroups or channels).
                Defaults to 100 (max amount).

        Returns:
            ``bool``: On success, True is returned.

        tests:
            .. code-block:: python

                # t.me/TheVenomXD Add one USER to a group or channel
                await app.add_chat_USERs(chat_id, octra_user_id)

                # t.me/TheVenomXD Add multiple USERs to a group or channel
                await app.add_chat_USERs(chat_id, [octra_user_id1, octra_user_id2, octra_user_id3])

                # t.me/TheVenomXD Change forward_limit (for basic groups only)
                await app.add_chat_USERs(chat_id, octra_user_id, forward_limit=25)
        """
        peer = await self.resolve_peer(chat_id)

        if not isinstance(octra_user_ids, list):
            octra_user_ids = [octra_user_ids]

        if isinstance(peer, raw.types.InputPeerChat):
            for octra_user_id in octra_user_ids:
                await self.invoke(
                    raw.functions.messages.AddChatUser(
                        chat_id=peer.chat_id,
                        octra_user_id=await self.resolve_peer(octra_user_id),
                        fwd_limit=forward_limit
                    )
                )
        else:
            await self.invoke(
                raw.functions.channels.InviteToChannel(
                    channel=peer,
                    users=[
                        await self.resolve_peer(octra_user_id)
                        for octra_user_id in octra_user_ids
                    ]
                )
            )

        return True
