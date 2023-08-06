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


class VideoNote(Object):
    """A video note.

    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.

        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different accounts.
            Can't be used to download or reuse the file.

        length (``int``):
            Video width and height as defined by sender.

        duration (``int``):
            Duration of the video in seconds as defined by sender.

        mime_type (``str``, *optional*):
            MIME type of the file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the video note was sent.

        thumbs (List of :obj:`~Octra.types.Thumbnail`, *optional*):
            Video thumbnails.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        file_id: str,
        file_unique_id: str,
        length: int,
        duration: int,
        thumbs: List["types.Thumbnail"] = None,
        mime_type: str = None,
        file_size: int = None,
        date: datetime = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.length = length
        self.duration = duration
        self.thumbs = thumbs

    @staticmethod
    def _parse(
        client,
        video_note: "raw.types.Document",
        video_attributes: "raw.types.DocumentAttributeVideo"
    ) -> "VideoNote":
        return VideoNote(
            file_id=FileId(
                file_type=FileType.VIDEO_NOTE,
                octra_dc_id_=video_note.octra_dc_id_,
                media_id=video_note.id,
                access_hash=video_note.access_hash,
                file_reference=video_note.file_reference
            ).encode(),
            file_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT,
                media_id=video_note.id
            ).encode(),
            length=video_attributes.w,
            duration=video_attributes.duration,
            file_size=video_note.size,
            mime_type=video_note.mime_type,
            date=utils.timestamp_to_datetime(video_note.date),
            thumbs=types.Thumbnail._parse(client, video_note),
            client=client
        )
