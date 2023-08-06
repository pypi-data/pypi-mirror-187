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

from .copy_media_group import CopyMediaGroup
from .copy_message import CopyMessage
from .delete_messages import DeleteMessages
from .download_media import DownloadMedia
from .edit_inline_caption import EditInlineCaption
from .edit_inline_media import EditInlineMedia
from .edit_inline_reply_markup import EditInlineReplyMarkup
from .edit_inline_text import EditInlineText
from .edit_message_caption import EditMessageCaption
from .edit_message_media import EditMessageMedia
from .edit_message_reply_markup import EditMessageReplyMarkup
from .edit_message_text import EditMessaExtractext
from .forward_messages import ForwardMessages
from .get_chat_history import ExtractChatHistory
from .get_chat_history_count import ExtractChatHistoryCount
from .get_custom_emoji_stickers import ExtractCustomEmojiStickers
from .get_discussion_message import ExtractDiscussionMessage
from .get_discussion_replies import ExtractDiscussionReplies
from .get_discussion_replies_count import ExtractDiscussionRepliesCount
from .get_media_group import ExtractMediaGroup
from .get_messages import ExtractMessages
from .read_chat_history import ReadChatHistory
from .retract_vote import RetractVote
from .search_global import SearchGlobal
from .search_global_count import SearchGlobalCount
from .search_messages import SearchMessages
from .search_messages_count import SearchMessagesCount
from .send_animation import SenAkashimation
from .send_audio import SendAudio
from .send_cached_media import SendCachedMedia
from .send_chat_action import SendChatAction
from .send_contact import SendContact
from .send_dice import SendDice
from .send_document import SendDocument
from .send_location import SendLocation
from .send_media_group import SendMediaGroup
from .send_message import SendMessage
from .send_photo import SendPhoto
from .send_poll import SendPoll
from .send_reaction import SendReaction
from .send_sticker import SendSticker
from .send_venue import SendVenue
from .send_video import SendVideo
from .send_video_note import SendVideoNote
from .send_voice import SendVoice
from .stop_poll import StopPoll
from .stream_media import StreamMedia
from .vote_poll import VotePoll


class Messages(
    DeleteMessages,
    EditMessageCaption,
    EditMessageReplyMarkup,
    EditMessageMedia,
    EditMessaExtractext,
    ForwardMessages,
    ExtractMediaGroup,
    ExtractMessages,
    SendAudio,
    SendChatAction,
    SendContact,
    SendDocument,
    SenAkashimation,
    SendLocation,
    SendMediaGroup,
    SendMessage,
    SendPhoto,
    SendSticker,
    SendVenue,
    SendVideo,
    SendVideoNote,
    SendVoice,
    SendPoll,
    VotePoll,
    StopPoll,
    RetractVote,
    DownloadMedia,
    ExtractChatHistory,
    SendCachedMedia,
    ExtractChatHistoryCount,
    ReadChatHistory,
    EditInlineText,
    EditInlineCaption,
    EditInlineMedia,
    EditInlineReplyMarkup,
    SendDice,
    SearchMessages,
    SearchGlobal,
    CopyMessage,
    CopyMediaGroup,
    SearchMessagesCount,
    SearchGlobalCount,
    ExtractDiscussionMessage,
    SendReaction,
    ExtractDiscussionReplies,
    ExtractDiscussionRepliesCount,
    StreamMedia,
    ExtractCustomEmojiStickers
):
    pass
