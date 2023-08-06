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

import Octra
from Octra import raw, utils
from Octra.file_id import FileId, FileType, FileUniqueId, FileUniqueType
from ..object import Object


class Voice(Object):
    """A voice note.

    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.

        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different accounts.
            Can't be used to download or reuse the file.

        duration (``int``):
            Duration of the audio in seconds as defined by sender.

        waveform (``bytes``, *optional*):
            Voice waveform.

        mime_type (``str``, *optional*):
            MIME type of the file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the voice was sent.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        file_id: str,
        file_unique_id: str,
        duration: int,
        waveform: bytes = None,
        mime_type: str = None,
        file_size: int = None,
        date: datetime = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.waveform = waveform
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date

    @staticmethod
    def _parse(client, voice: "raw.types.Document", attributes: "raw.types.DocumentAttributeAudio") -> "Voice":
        return Voice(
            file_id=FileId(
                file_type=FileType.VOICE,
                octra_dc_id_=voice.octra_dc_id_,
                media_id=voice.id,
                access_hash=voice.access_hash,
                file_reference=voice.file_reference
            ).encode(),
            file_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT,
                media_id=voice.id
            ).encode(),
            duration=attributes.duration,
            mime_type=voice.mime_type,
            file_size=voice.size,
            waveform=attributes.waveform,
            date=utils.timestamp_to_datetime(voice.date),
            client=client
        )
