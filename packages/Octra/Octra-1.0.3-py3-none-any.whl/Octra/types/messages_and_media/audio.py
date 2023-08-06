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


class Audio(Object):
    """An audio file to be treated as music by the Telegram clients.

    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.

        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different accounts.
            Can't be used to download or reuse the file.

        duration (``int``):
            Duration of the audio in seconds as defined by sender.

        performer (``str``, *optional*):
            Performer of the audio as defined by sender or by audio tags.

        title (``str``, *optional*):
            Title of the audio as defined by sender or by audio tags.

        file_name (``str``, *optional*):
            Audio file name.

        mime_type (``str``, *optional*):
            MIME type of the file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the audio was originally sent.

        thumbs (List of :obj:`~Octra.types.Thumbnail`, *optional*):
            Thumbnails of the music file album cover.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        file_id: str,
        file_unique_id: str,
        duration: int,
        performer: str = None,
        title: str = None,
        file_name: str = None,
        mime_type: str = None,
        file_size: int = None,
        date: datetime = None,
        thumbs: List["types.Thumbnail"] = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.performer = performer
        self.title = title
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.thumbs = thumbs

    @staticmethod
    def _parse(
        client,
        audio: "raw.types.Document",
        audio_attributes: "raw.types.DocumentAttributeAudio",
        file_name: str
    ) -> "Audio":
        return Audio(
            file_id=FileId(
                file_type=FileType.AUDIO,
                octra_dc_id_=audio.octra_dc_id_,
                media_id=audio.id,
                access_hash=audio.access_hash,
                file_reference=audio.file_reference
            ).encode(),
            file_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT,
                media_id=audio.id
            ).encode(),
            duration=audio_attributes.duration,
            performer=audio_attributes.performer,
            title=audio_attributes.title,
            mime_type=audio.mime_type,
            file_size=audio.size,
            file_name=file_name,
            date=utils.timestamp_to_datetime(audio.date),
            thumbs=types.Thumbnail._parse(client, audio),
            client=client
        )
