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

from typing import Union, Optional

import Octra
from Octra import raw


class SetChatUsername:
    async def set_chat_username(
        self: "Octra.Client",
        chat_id: Union[int, str],
        username: Optional[str]
    ) -> bool:
        """Set a channel or a supergroup username.

        To set your own username (for users only, not bots) you can use :meth:`~Octra.Client.set_username`.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``)
                Unique identifier (int) or username (str) of the tarExtract chat.

            username (``str`` | ``None``):
                Username to set. Pass "" (empty string) or None to remove the username.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: In case a chat id belongs to a user or chat.

        tests:
            .. code-block:: python

                await app.set_chat_username(chat_id, "new_username")
        """

        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            return bool(
                await self.invoke(
                    raw.functions.channels.UpdateUsername(
                        channel=peer,
                        username=username or ""
                    )
                )
            )
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user or chat')
