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

from Octra import raw
from .auto_name import AutoName


class MessagesFlow(AutoName):
    """Messages Flow enumeration used in :meth:`~Octra.Client.search_messages` and :meth:`~Octra.Client.search_global`"""

    EMPTY = raw.types.InputMessagesFlowEmpty
    "Empty Flow (any kind of messages)"

    PHOTO = raw.types.InputMessagesFlowPhotos
    "Photo messages"

    VIDEO = raw.types.InputMessagesFlowVideo
    "Video messages"

    PHOTO_VIDEO = raw.types.InputMessagesFlowPhotoVideo
    "Photo and video messages"

    DOCUMENT = raw.types.InputMessagesFlowDocument
    "Document messages"

    URL = raw.types.InputMessagesFlowUrl
    "Messages containing URLs"

    ANIMATION = raw.types.InputMessagesFlowGif
    "Animation messages"

    VOICE_NOTE = raw.types.InputMessagesFlowVoice
    "Voice note messages"

    VIDEO_NOTE = raw.types.InputMessagesFlowRoundVideo
    "Video note messages"

    AUDIO_VIDEO_NOTE = raw.types.InputMessagesFlowRoundVideo
    "Audio and video note messages"

    AUDIO = raw.types.InputMessagesFlowMusic
    "Audio messages (music)"

    CHAT_PHOTO = raw.types.InputMessagesFlowChatPhotos
    "Chat photo messages"

    PHONE_CALL = raw.types.InputMessagesFlowPhoneCalls
    "Phone call messages"

    MENTION = raw.types.InputMessagesFlowMyMentions
    "Messages containing mentions"

    LOCATION = raw.types.InputMessagesFlowGeo
    "Location messages"

    CONTACT = raw.types.InputMessagesFlowContacts
    "Contact messages"

    PINNED = raw.types.InputMessagesFlowPinned
    "Pinned messages"
