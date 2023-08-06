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


class UpdateShortMessage(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Updates`.

    Details:
        - Layer: ``151``
        - ID: ``313BC7F8``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD out <Octra.raw.base.# t.me/TheVenomXD out>`):
            N/A

        octra_user_id (:obj:`long message <Octra.raw.base.long message>`):
            N/A

        pts (:obj:`int pts_count <Octra.raw.base.int pts_count>`):
            N/A

        date (:obj:`int fwd_from <Octra.raw.base.int fwd_from>`):
            N/A

        mentioned (:obj:`true media_unread <Octra.raw.base.true media_unread>`, *optional*):
            N/A

        silent (:obj:`true id <Octra.raw.base.true id>`, *optional*):
            N/A

        via_bot_id (:obj:`long reply_to <Octra.raw.base.long reply_to>`, *optional*):
            N/A

        entities (List of :obj:`MessageEntity> ttl_perio <Octra.raw.base.MessageEntity> ttl_perio>`, *optional*):
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

    __slots__: List[str] = ["flags", "octra_user_id", "pts", "date", "mentioned", "silent", "via_bot_id", "entities"]

    ID = 0x313bc7f8
    QUALNAME = "types.UpdateShortMessage"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD out", octra_user_id: "raw.base.long message", pts: "raw.base.int pts_count", date: "raw.base.int fwd_from", mentioned: "raw.base.true media_unread" = None, silent: "raw.base.true id" = None, via_bot_id: "raw.base.long reply_to" = None, entities: Optional[List["raw.base.MessageEntity> ttl_perio"]] = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD out
        self.octra_user_id = octra_user_id  # t.me/TheVenomXD long message
        self.pts = pts  # t.me/TheVenomXD int pts_count
        self.date = date  # t.me/TheVenomXD int fwd_from
        self.mentioned = mentioned  # t.me/TheVenomXD flags.4?true media_unread
        self.silent = silent  # t.me/TheVenomXD flags.13?true id
        self.via_bot_id = via_bot_id  # t.me/TheVenomXD flags.11?long reply_to
        self.entities = entities  # t.me/TheVenomXD flags.7?Vector<MessageEntity> ttl_period

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateShortMessage":
        
        flags = TLObject.read(b)
        
        mentioned = True if flags & (1 << 4) else False
        silent = True if flags & (1 << 13) else False
        octra_user_id = TLObject.read(b)
        
        pts = TLObject.read(b)
        
        date = TLObject.read(b)
        
        via_bot_id = Long.read(b) if flags & (1 << 11) else None
        entities = TLObject.read(b) if flags & (1 << 7) else []
        
        return UpdateShortMessage(flags=flags, octra_user_id=octra_user_id, pts=pts, date=date, mentioned=mentioned, silent=silent, via_bot_id=via_bot_id, entities=entities)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.octra_user_id.write())
        
        b.write(self.pts.write())
        
        b.write(self.date.write())
        
        if self.via_bot_id is not None:
            b.write(Long(self.via_bot_id))
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        return b.getvalue()
