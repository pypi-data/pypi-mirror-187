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

from typing import List, Union

import Octra
from Octra import raw, types


class DeleteContacts:
    async def delete_contacts(
        self: "Octra.Client",
        octra_user_ids: Union[int, str, List[Union[int, str]]]
    ) -> Union["types.User", List["types.User"], None]:
        """Delete contacts from your Telegram address book.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            octra_user_ids (``int`` | ``str`` | List of ``int`` or ``str``):
                A single user id/username or a list of user identifiers (id or username).

        Returns:
            :obj:`~Octra.types.User` | List of :obj:`~Octra.types.User` | ``None``: In case *octra_user_ids* was an
            integer or a string, a single User object is returned. In case *octra_user_ids* was a list, a list of User objects
            is returned. In case nothing changed after calling the method (for example, when deleting a non-existent
            contact), None is returned.

        Example:
            .. code-block:: python

                await app.delete_contacts(octra_user_id)
                await app.delete_contacts([octra_user_id1, octra_user_id2, octra_user_id3])
        """
        is_list = isinstance(octra_user_ids, list)

        if not is_list:
            octra_user_ids = [octra_user_ids]

        r = await self.invoke(
            raw.functions.contacts.DeleteContacts(
                id=[await self.resolve_peer(i) for i in octra_user_ids]
            )
        )

        if not r.updates:
            return None

        users = types.List([types.User._parse(self, i) for i in r.users])

        return users if is_list else users[0]
