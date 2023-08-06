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

from datetime import datetime
from typing import List

import Octra
from Octra import raw, utils
from Octra import types
from Octra.file_id import FileId, FileType, FileUniqueId, FileUniqueType
from ..object import Object


class Animation(Object):
    """An animation file (GIF or H.264/MPEG-4 AVC video without sound).

    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.

        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different accounts.
            Can't be used to download or reuse the file.

        width (``int``):
            Animation width as defined by sender.

        height (``int``):
            Animation height as defined by sender.

        duration (``int``):
            Duration of the animation in seconds as defined by sender.

        file_name (``str``, *optional*):
            Animation file name.

        mime_type (``str``, *optional*):
            Mime type of a file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the animation was sent.

        thumbs (List of :obj:`~Octra.types.Thumbnail`, *optional*):
            Animation thumbnails.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        file_id: str,
        file_unique_id: str,
        width: int,
        height: int,
        duration: int,
        file_name: str = None,
        mime_type: str = None,
        file_size: int = None,
        date: datetime = None,
        thumbs: List["types.Thumbnail"] = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.width = width
        self.height = height
        self.duration = duration
        self.thumbs = thumbs

    @staticmethod
    def _parse(
        client,
        animation: "raw.types.Document",
        video_attributes: "raw.types.DocumentAttributeVideo",
        file_name: str
    ) -> "Animation":
        return Animation(
            file_id=FileId(
                file_type=FileType.ANIMATION,
                octra_dc_id_=animation.octra_dc_id_,
                media_id=animation.id,
                access_hash=animation.access_hash,
                file_reference=animation.file_reference
            ).encode(),
            file_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT,
                media_id=animation.id
            ).encode(),
            width=getattr(video_attributes, "w", 0),
            height=getattr(video_attributes, "h", 0),
            duration=getattr(video_attributes, "duration", 0),
            mime_type=animation.mime_type,
            file_size=animation.size,
            file_name=file_name,
            date=utils.timestamp_to_datetime(animation.date),
            thumbs=types.Thumbnail._parse(client, animation),
            client=client
        )
