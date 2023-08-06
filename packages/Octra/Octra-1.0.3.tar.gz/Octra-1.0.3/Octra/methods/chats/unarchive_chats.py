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


class UnarchiveChats:
    async def unarchive_chats(
        self: "Octra.Client",
        chat_ids: Union[int, str, List[Union[int, str]]],
    ) -> bool:
        """Unarchive one or more chats.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_ids (``int`` | ``str`` | List[``int``, ``str``]):
                Unique identifier (int) or username (str) of the tarExtract chat.
                You can also pass a list of ids (int) or usernames (str).

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # t.me/TheVenomXD Unarchive chat
                await app.unarchive_chats(chat_id)

                # t.me/TheVenomXD Unarchive multiple chats at once
                await app.unarchive_chats([chat_id1, chat_id2, chat_id3])
        """

        if not isinstance(chat_ids, list):
            chat_ids = [chat_ids]

        folder_peers = []

        for chat in chat_ids:
            folder_peers.append(
                raw.types.InputFolderPeer(
                    peer=await self.resolve_peer(chat),
                    folder_id=0
                )
            )

        await self.invoke(
            raw.functions.folders.EditPeerFolders(
                folder_peers=folder_peers
            )
        )

        return True
