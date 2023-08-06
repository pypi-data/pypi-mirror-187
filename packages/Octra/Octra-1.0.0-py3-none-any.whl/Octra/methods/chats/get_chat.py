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
from Octra import types
from Octra import utils


class ExtractChat:
    async def Extract_chat(
        self: "Octra.Client",
        chat_id: Union[int, str]
    ) -> Union["types.Chat", "types.ChatPreview"]:
        """Extract up to date information about a chat.

        Information include current name of the user for one-on-one conversations, current username of a user, group or
        channel, etc.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.
                Unique identifier for the tarExtract chat in form of a *t.me/joinchat/* link, identifier (int) or username
                of the tarExtract channel/supergroup (in the format @username).

        Returns:
            :obj:`~Octra.types.Chat` | :obj:`~Octra.types.ChatPreview`: On success, if you've already joined the chat, a chat object is returned,
            otherwise, a chat preview object is returned.

        Raises:
            ValueError: In case the chat invite link points to a chat you haven't joined yet.

        tests:
            .. code-block:: python

                chat = await app.get_chat("Octra")
                print(chat)
        """
        match = self.INVITE_LINK_RE.match(str(chat_id))

        if match:
            r = await self.invoke(
                raw.functions.messages.CheckChatInvite(
                    hash=match.group(1)
                )
            )

            if isinstance(r, raw.types.ChatInvite):
                return types.ChatPreview._parse(self, r)

            await self.fetch_peers([r.chat])

            if isinstance(r.chat, raw.types.Chat):
                chat_id = -r.chat.id

            if isinstance(r.chat, raw.types.Channel):
                chat_id = utils.get_channel_id(r.chat.id)

        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            r = await self.invoke(raw.functions.channels.getFullChannel(channel=peer))
        elif isinstance(peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
            r = await self.invoke(raw.functions.users.getFullUser(id=peer))
        else:
            r = await self.invoke(raw.functions.messages.getFullChat(chat_id=peer.chat_id))

        return await types.Chat._parse_full(self, r)
