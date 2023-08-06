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

from typing import Union

import Octra
from Octra import raw


class SetChatTitle:
    async def set_chat_title(
        self: "Octra.Client",
        chat_id: Union[int, str],
        title: str
    ) -> bool:
        """Change the title of a chat.
        Titles can't be changed for private chats.
        You must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Note:
            In regular groups (non-supergroups), this method will only work if the "All USERs Are Admins"
            setting is off.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

            title (``str``):
                New chat title, 1-255 characters.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: In case a chat id belongs to user.

        Example:
            .. code-block:: python

                await app.set_chat_title(chat_id, "New Title")
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChat):
            await self.invoke(
                raw.functions.messages.EditChatTitle(
                    chat_id=peer.chat_id,
                    title=title
                )
            )
        elif isinstance(peer, raw.types.InputPeerChannel):
            await self.invoke(
                raw.functions.channels.EditTitle(
                    channel=peer,
                    title=title
                )
            )
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')

        return True
