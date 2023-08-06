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

from .animation import Animation
from .audio import Audio
from .contact import Contact
from .dice import Dice
from .document import Document
from .game import Game
from .location import Location
from .message import Message
from .message_entity import MessageEntity
from .photo import Photo
from .poll import Poll
from .poll_option import PollOption
from .reaction import Reaction
from .sticker import Sticker
from .stripped_thumbnail import StrippedThumbnail
from .thumbnail import Thumbnail
from .venue import Venue
from .video import Video
from .video_note import VideoNote
from .voice import Voice
from .web_app_data import WebAppData
from .web_page import WebPage
from .message_reactions import MessageReactions

__all__ = [
    "Animation", "Audio", "Contact", "Document", "Game", "Location", "Message", "MessageEntity", "Photo", "Thumbnail",
    "StrippedThumbnail", "Poll", "PollOption", "Sticker", "Venue", "Video", "VideoNote", "Voice", "WebPage", "Dice",
    "Reaction", "WebAppData", "MessageReactions"
]
