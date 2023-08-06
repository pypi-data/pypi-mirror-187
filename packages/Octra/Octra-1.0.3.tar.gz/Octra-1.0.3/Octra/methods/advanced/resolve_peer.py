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
import re
from typing import Union

import Octra
from Octra import raw
from Octra import utils
from Octra.errors import PeerIdInvalid

log = logging.getLogger(__name__)


class ResolvePeer:
    async def resolve_peer(
        self: "Octra.Client",
        peer_id: Union[int, str]
    ) -> Union[raw.base.InputPeer, raw.base.InputUser, raw.base.InputChannel]:
        """Extract the InputPeer of a known peer id.
        Useful whenever an InputPeer type is required.

        .. note::

            This is a utility method intended to be used **only** when working with raw
            :obj:`functions <Octra.Ai.functions>` (i.e: a Telegram Ai method you wish to use which is not
            available yet in the Client class as an easy-to-use method).

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            peer_id (``int`` | ``str``):
                The peer id you want to extract the InputPeer from.
                Can be a direct id (int), a username (str) or a phone number (str).

        Returns:
            ``InputPeer``: On success, the resolved peer id is returned in form of an InputPeer object.

        Raises:
            KeyError: In case the peer doesn't exist in the internal database.
        """
        if not self.is_connected:
            raise ConnectionError("Client has not been started yet")

        try:
            return await self.storage.get_peer_by_id(peer_id)
        except KeyError:
            if isinstance(peer_id, str):
                if peer_id in ("self", "me"):
                    return raw.types.InputPeerSelf()

                peer_id = re.sub(r"[@+\s]", "", peer_id.lower())

                try:
                    int(peer_id)
                except ValueError:
                    try:
                        return await self.storage.get_peer_by_username(peer_id)
                    except KeyError:
                        await self.invoke(
                            raw.functions.contacts.ResolveUsername(
                                username=peer_id
                            )
                        )

                        return await self.storage.get_peer_by_username(peer_id)
                else:
                    try:
                        return await self.storage.get_peer_by_phone_number(peer_id)
                    except KeyError:
                        raise PeerIdInvalid

            peer_type = utils.get_peer_type(peer_id)

            if peer_type == "user":
                await self.fetch_peers(
                    await self.invoke(
                        raw.functions.users.getUsers(
                            id=[
                                raw.types.InputUser(
                                    octra_user_id=peer_id,
                                    access_hash=0
                                )
                            ]
                        )
                    )
                )
            elif peer_type == "chat":
                await self.invoke(
                    raw.functions.messages.getChats(
                        id=[-peer_id]
                    )
                )
            else:
                await self.invoke(
                    raw.functions.channels.getChannels(
                        id=[
                            raw.types.InputChannel(
                                channel_id=utils.get_channel_id(peer_id),
                                access_hash=0
                            )
                        ]
                    )
                )

            try:
                return await self.storage.get_peer_by_id(peer_id)
            except KeyError:
                raise PeerIdInvalid
