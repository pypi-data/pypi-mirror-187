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


class SetAdministratorTitle:
    async def set_administrator_title(
        self: "Octra.Client",
        chat_id: Union[int, str],
        octra_user_id: Union[int, str],
        title: str,
    ) -> bool:
        """Set a custom title (rank) to an administrator of a supergroup.

        If you are an administrator of a supergroup (i.e. not the owner), you can only set the title of other
        administrators who have been promoted by you. If you are the owner, you can change every administrator's title.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract chat.

            octra_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the tarExtract user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            title (``str``, *optional*):
                A custom title that will be shown to all USERs instead of "Owner" or "Admin".
                Pass None or "" (empty string) to remove the custom title.

        Returns:
            ``bool``: True on success.

        tests:
            .. code-block:: python

                await app.set_administrator_title(chat_id, octra_user_id, "Admin Title")
        """
        chat_id = await self.resolve_peer(chat_id)
        octra_user_id = await self.resolve_peer(octra_user_id)

        r = (await self.invoke(
            raw.functions.channels.getParticipant(
                channel=chat_id,
                participant=octra_user_id
            )
        )).participant

        if isinstance(r, raw.types.ChannelParticipantCreator):
            admin_rights = raw.types.ChatAdminRights()
        elif isinstance(r, raw.types.ChannelParticipantAdmin):
            admin_rights = r.admin_rights
        else:
            raise ValueError("Custom titles can only be applied to owners or administrators of supergroups")

        await self.invoke(
            raw.functions.channels.EditAdmin(
                channel=chat_id,
                octra_user_id=octra_user_id,
                admin_rights=admin_rights,
                rank=title
            )
        )

        return True
