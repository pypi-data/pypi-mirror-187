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

from io import BytesIO

from Octra.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from Octra.raw.core import TLObject
from Octra import raw
from typing import List, Optional, Any

# t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD
# t.me/TheVenomXD               !!! WARNING !!!               # t.me/TheVenomXD
# t.me/TheVenomXD          This is a generated file!          # t.me/TheVenomXD
# t.me/TheVenomXD All changes made in this file will be lost! # t.me/TheVenomXD
# t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD


class UpdateShortChatMessage(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Updates`.

    Details:
        - Layer: ``151``
        - ID: ``4D6DEEA5``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD out <Octra.raw.base.# t.me/TheVenomXD out>`):
            N/A

        from_id (:obj:`long chat_id <Octra.raw.base.long chat_id>`):
            N/A

        message (:obj:`string pts <Octra.raw.base.string pts>`):
            N/A

        pts_count (:obj:`int date <Octra.raw.base.int date>`):
            N/A

        mentioned (:obj:`true media_unread <Octra.raw.base.true media_unread>`, *optional*):
            N/A

        silent (:obj:`true id <Octra.raw.base.true id>`, *optional*):
            N/A

        fwd_from (:obj:`MessageFwdHeader via_bot_id <Octra.raw.base.MessageFwdHeader via_bot_id>`, *optional*):
            N/A

        reply_to (:obj:`MessageReplyHeader entities <Octra.raw.base.MessageReplyHeader entities>`, *optional*):
            N/A

        ttl_period (:obj:`int  <Octra.raw.base.int >`, *optional*):
            N/A

    Functions:
        This object can be returned by 83 functions.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetNotifyExceptions
            contacts.DeleteContacts
            contacts.AddContact
            contacts.AcceptContact
            contacts.GetLocated
            contacts.BlockFromReplies
            messages.SendMessage
            messages.SendMedia
            messages.ForwardMessages
            messages.EditChatTitle
            messages.EditChatPhoto
            messages.AddChatUser
            messages.DeleteChatUser
            messages.CreateChat
            messages.ImportChatInvite
            messages.StartBot
            messages.MigrateChat
            messages.SendInlineBotResult
            messages.EditMessage
            messages.GetAllDrafts
            messages.SetGameScore
            messages.SendScreenshotNotification
            messages.SendMultiMedia
            messages.UpdatePinnedMessage
            messages.SendVote
            messages.GetPollResults
            messages.EditChatDefaultBannedRights
            messages.SendScheduledMessages
            messages.DeleteScheduledMessages
            messages.SetHistoryTTL
            messages.SetChatTheme
            messages.HideChatJoinRequest
            messages.HideAllChatJoinRequests
            messages.ToggleNoForwards
            messages.SendReaction
            messages.GetMessagesReactions
            messages.SetChatAvailableReactions
            messages.SendWebViewData
            messages.GetExtendedMedia
            help.GetAppChangelog
            channels.CreateChannel
            channels.EditAdmin
            channels.EditTitle
            channels.EditPhoto
            channels.JoinChannel
            channels.LeaveChannel
            channels.InviteToChannel
            channels.DeleteChannel
            channels.ToggleSignatures
            channels.EditBanned
            channels.DeleteHistory
            channels.TogglePreHistoryHidden
            channels.EditCreator
            channels.ToggleSlowMode
            channels.ConvertToGigagroup
            channels.ToggleJoinToSend
            channels.ToggleJoinRequest
            channels.ToggleForum
            channels.CreateForumTopic
            channels.EditForumTopic
            channels.UpdatePinnedForumTopic
            channels.ReorderPinnedForumTopics
            channels.ToggleAntiSpam
            channels.ToggleParticipantsHidden
            payments.AssignAppStoreTransaction
            payments.AssignPlayMarketTransaction
            phone.DiscardCall
            phone.SetCallRating
            phone.CreateGroupCall
            phone.JoinGroupCall
            phone.LeaveGroupCall
            phone.InviteToGroupCall
            phone.DiscardGroupCall
            phone.ToggleGroupCallSettings
            phone.ToggleGroupCallRecord
            phone.EditGroupCallParticipant
            phone.EditGroupCallTitle
            phone.ToggleGroupCallStartSubscription
            phone.StartScheduledGroupCall
            phone.JoinGroupCallPresentation
            phone.LeaveGroupCallPresentation
            folders.EditPeerFolders
            folders.DeleteFolder
    """

    __slots__: List[str] = ["flags", "from_id", "message", "pts_count", "mentioned", "silent", "fwd_from", "reply_to", "ttl_period"]

    ID = 0x4d6deea5
    QUALNAME = "types.UpdateShortChatMessage"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD out", from_id: "raw.base.long chat_id", message: "raw.base.string pts", pts_count: "raw.base.int date", mentioned: "raw.base.true media_unread" = None, silent: "raw.base.true id" = None, fwd_from: "raw.base.MessageFwdHeader via_bot_id" = None, reply_to: "raw.base.MessageReplyHeader entities" = None, ttl_period: "raw.base.int " = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD out
        self.from_id = from_id  # t.me/TheVenomXD long chat_id
        self.message = message  # t.me/TheVenomXD string pts
        self.pts_count = pts_count  # t.me/TheVenomXD int date
        self.mentioned = mentioned  # t.me/TheVenomXD flags.4?true media_unread
        self.silent = silent  # t.me/TheVenomXD flags.13?true id
        self.fwd_from = fwd_from  # t.me/TheVenomXD flags.2?MessageFwdHeader via_bot_id
        self.reply_to = reply_to  # t.me/TheVenomXD flags.3?MessageReplyHeader entities
        self.ttl_period = ttl_period  # t.me/TheVenomXD flags.25?int 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateShortChatMessage":
        
        flags = TLObject.read(b)
        
        mentioned = True if flags & (1 << 4) else False
        silent = True if flags & (1 << 13) else False
        from_id = TLObject.read(b)
        
        message = TLObject.read(b)
        
        pts_count = TLObject.read(b)
        
        fwd_from = TLObject.read(b) if flags & (1 << 2) else None
        
        reply_to = TLObject.read(b) if flags & (1 << 3) else None
        
        ttl_period = Int.read(b) if flags & (1 << 25) else None
        return UpdateShortChatMessage(flags=flags, from_id=from_id, message=message, pts_count=pts_count, mentioned=mentioned, silent=silent, fwd_from=fwd_from, reply_to=reply_to, ttl_period=ttl_period)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.from_id.write())
        
        b.write(self.message.write())
        
        b.write(self.pts_count.write())
        
        if self.fwd_from is not None:
            b.write(self.fwd_from.write())
        
        if self.reply_to is not None:
            b.write(self.reply_to.write())
        
        if self.ttl_period is not None:
            b.write(Int(self.ttl_period))
        
        return b.getvalue()
