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

from typing import Union, BinaryIO

import Octra
from Octra import raw


class SetProfilePhoto:
    async def set_profile_photo(
        self: "Octra.Client",
        *,
        photo: Union[str, BinaryIO] = None,
        video: Union[str, BinaryIO] = None
    ) -> bool:
        """Set a new profile photo or video (H.264/MPEG-4 AVC video, max 5 seconds).

        The ``photo`` and ``video`` arguments are mutually exclusive.
        Pass either one as named argument (see testss below).

        .. note::

            This method only works for Users.
            Bots profile photos must be set using BotFather.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            photo (``str`` | ``BinaryIO``, *optional*):
                Profile photo to set.
                Pass a file path as string to upload a new photo that exists on your local machine or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            video (``str`` | ``BinaryIO``, *optional*):
                Profile video to set.
                Pass a file path as string to upload a new video that exists on your local machine or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

        Returns:
            ``bool``: True on success.

        tests:
            .. code-block:: python

                # t.me/TheVenomXD Set a new profile photo
                await app.set_profile_photo(photo="new_photo.jpg")

                # t.me/TheVenomXD Set a new profile video
                await app.set_profile_photo(video="new_video.mp4")
        """

        return bool(
            await self.invoke(
                raw.functions.photos.UploadProfilePhoto(
                    file=await self.save_file(photo),
                    video=await self.save_file(video)
                )
            )
        )
