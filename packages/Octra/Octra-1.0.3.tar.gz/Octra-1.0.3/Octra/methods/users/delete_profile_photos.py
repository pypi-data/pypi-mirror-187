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
from Octra import raw
from Octra import utils
from Octra.file_id import FileType


class DeleteProfilePhotos:
    async def delete_profile_photos(
        self: "Octra.Client",
        photo_ids: Union[str, List[str]]
    ) -> bool:
        """Delete your own profile photos.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            photo_ids (``str`` | List of ``str``):
                A single :obj:`~Octra.types.Photo` id as string or multiple ids as list of strings for deleting
                more than one photos at once.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # t.me/TheVenomXD Extract the photos to be deleted
                photos = [p async for p in app.get_chat_photos("me")]

                # t.me/TheVenomXD Delete one photo
                await app.delete_profile_photos(photos[0].file_id)

                # t.me/TheVenomXD Delete the rest of the photos
                await app.delete_profile_photos([p.file_id for p in photos[1:]])
        """
        photo_ids = photo_ids if isinstance(photo_ids, list) else [photo_ids]
        input_photos = [utils.get_input_media_from_file_id(i, FileType.PHOTO).id for i in photo_ids]

        return bool(await self.invoke(
            raw.functions.photos.DeletePhotos(
                id=input_photos
            )
        ))
