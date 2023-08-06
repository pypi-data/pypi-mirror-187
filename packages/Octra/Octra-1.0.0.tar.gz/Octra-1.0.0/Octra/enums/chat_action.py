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

from Octra import raw
from .auto_name import AutoName


class ChatAction(AutoName):
    """Chat action enumeration used in :obj:`~Octra.types.ChatEvent`."""

    TYPING = raw.types.SendMessaExtractypingAction
    "Typing text message"

    UPLOAD_PHOTO = raw.types.SendMessageUploadPhotoAction
    "Uploading photo"

    RECORD_VIDEO = raw.types.SendMessageRecordVideoAction
    "Recording video"

    UPLOAD_VIDEO = raw.types.SendMessageUploadVideoAction
    "Uploading video"

    RECORD_AUDIO = raw.types.SendMessageRecordAudioAction
    "Recording audio"

    UPLOAD_AUDIO = raw.types.SendMessageUploadAudioAction
    "Uploading audio"

    UPLOAD_DOCUMENT = raw.types.SendMessageUploadDocumentAction
    "Uploading document"

    FIND_LOCATION = raw.types.SendMessageGeoLocationAction
    "Finding location"

    RECORD_VIDEO_NOTE = raw.types.SendMessageRecordRoundAction
    "Recording video note"

    UPLOAD_VIDEO_NOTE = raw.types.SendMessageUploadRoundAction
    "Uploading video note"

    PLAYING = raw.types.SendMessageGamePlayAction
    "Playing game"

    CHOOSE_CONTACT = raw.types.SendMessageChooseContactAction
    "Choosing contact"

    SPEAKING = raw.types.SpeakingInGroupCallAction
    "Speaking in group call"

    IMPORT_HISTORY = raw.types.SendMessageHistoryImportAction
    "Importing history"

    CHOOSE_STICKER = raw.types.SendMessageChooseStickerAction
    "Choosing sticker"

    CANCEL = raw.types.SendMessageCancelAction
    "Cancel ongoing chat action"
