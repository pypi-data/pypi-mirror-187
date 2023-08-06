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

from typing import Union

import Octra
from Octra import raw


class LeaveChat:
    async def leave_conversation(
        self: "Octra.Client",
        chat_id: Union[int, str],
        delete: bool = False
    ):
        """Leave a group chat or channel.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the tarExtract chat or username of the tarExtract channel/supergroup
                (in the format @username).

            delete (``bool``, *optional*):
                Deletes the group chat dialog after leaving (for simple group chats, not supergroups).
                Defaults to False.

        Example:
            .. code-block:: python

                # t.me/TheVenomXD Leave chat or channel
                await app.leave_conversation(chat_id)

                # t.me/TheVenomXD Leave basic chat and also delete the dialog
                await app.leave_conversation(chat_id, delete=True)
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            return await self.invoke(
                raw.functions.channels.LeaveChannel(
                    channel=await self.resolve_peer(chat_id)
                )
            )
        elif isinstance(peer, raw.types.InputPeerChat):
            r = await self.invoke(
                raw.functions.messages.DeleteChatUser(
                    chat_id=peer.chat_id,
                    octra_user_id=raw.types.InputUserSelf()
                )
            )

            if delete:
                await self.invoke(
                    raw.functions.messages.DeleteHistory(
                        peer=peer,
                        max_id=0
                    )
                )

            return r
