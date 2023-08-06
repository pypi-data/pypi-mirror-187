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

# t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD
# t.me/TheVenomXD               !!! WARNING !!!               # t.me/TheVenomXD
# t.me/TheVenomXD          This is a generated file!          # t.me/TheVenomXD
# t.me/TheVenomXD All changes made in this file will be lost! # t.me/TheVenomXD
# t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD

from typing import Union
from Octra import raw
from Octra.raw.core import TLObject

ChannelAdminLogEventAction = Union[raw.types.ChannelAdminLogEventActionChanExtractitle, raw.types.ChannelAdminLogEventActionChangeAbout, raw.types.ChannelAdminLogEventActionChangeAvailableReactions, raw.types.ChannelAdminLogEventActionChangeHistoryTTL, raw.types.ChannelAdminLogEventActionChangeLinkedChat, raw.types.ChannelAdminLogEventActionChangeLocation, raw.types.ChannelAdminLogEventActionChangePhoto, raw.types.ChannelAdminLogEventActionChangeStickerSet, raw.types.ChannelAdminLogEventActionChangeUsername, raw.types.ChannelAdminLogEventActionChangeUsernames, raw.types.ChannelAdminLogEventActionCreateTopic, raw.types.ChannelAdminLogEventActionDefaultBannedRights, raw.types.ChannelAdminLogEventActionDeleteMessage, raw.types.ChannelAdminLogEventActionDeleteTopic, raw.types.ChannelAdminLogEventActionDiscardGroupCall, raw.types.ChannelAdminLogEventActionEditMessage, raw.types.ChannelAdminLogEventActionEditTopic, raw.types.ChannelAdminLogEventActionExportedInviteDelete, raw.types.ChannelAdminLogEventActionExportedInviteEdit, raw.types.ChannelAdminLogEventActionExportedInviteRevoke, raw.types.ChannelAdminLogEventActionParticipantInvite, raw.types.ChannelAdminLogEventActionParticipantJoin, raw.types.ChannelAdminLogEventActionParticipantJoinByInvite, raw.types.ChannelAdminLogEventActionParticipantJoinByRequest, raw.types.ChannelAdminLogEventActionParticipantLeave, raw.types.ChannelAdminLogEventActionParticipantMute, raw.types.ChannelAdminLogEventActionParticipantToggleAdmin, raw.types.ChannelAdminLogEventActionParticipantToggleBan, raw.types.ChannelAdminLogEventActionParticipantUnmute, raw.types.ChannelAdminLogEventActionParticipantVolume, raw.types.ChannelAdminLogEventActionPinTopic, raw.types.ChannelAdminLogEventActionSendMessage, raw.types.ChannelAdminLogEventActionStartGroupCall, raw.types.ChannelAdminLogEventActionStopPoll, raw.types.ChannelAdminLogEventActionToggleAntiSpam, raw.types.ChannelAdminLogEventActionToggleForum, raw.types.ChannelAdminLogEventActionToggleGroupCallSetting, raw.types.ChannelAdminLogEventActionToggleInvites, raw.types.ChannelAdminLogEventActionToggleNoForwards, raw.types.ChannelAdminLogEventActionTogglePreHistoryHidden, raw.types.ChannelAdminLogEventActionToggleSignatures, raw.types.ChannelAdminLogEventActionToggleSlowMode, raw.types.ChannelAdminLogEventActionUpdatePinned]


# t.me/TheVenomXD noinspection PyRedeclaration
class ChannelAdminLogEventAction:  # t.me/TheVenomXD type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 43 constructors available.

        .. currentmodule:: Octra.raw.types

        .. autosummary::
            :nosignatures:

            ChannelAdminLogEventActionChanExtractitle
            ChannelAdminLogEventActionChangeAbout
            ChannelAdminLogEventActionChangeAvailableReactions
            ChannelAdminLogEventActionChangeHistoryTTL
            ChannelAdminLogEventActionChangeLinkedChat
            ChannelAdminLogEventActionChangeLocation
            ChannelAdminLogEventActionChangePhoto
            ChannelAdminLogEventActionChangeStickerSet
            ChannelAdminLogEventActionChangeUsername
            ChannelAdminLogEventActionChangeUsernames
            ChannelAdminLogEventActionCreateTopic
            ChannelAdminLogEventActionDefaultBannedRights
            ChannelAdminLogEventActionDeleteMessage
            ChannelAdminLogEventActionDeleteTopic
            ChannelAdminLogEventActionDiscardGroupCall
            ChannelAdminLogEventActionEditMessage
            ChannelAdminLogEventActionEditTopic
            ChannelAdminLogEventActionExportedInviteDelete
            ChannelAdminLogEventActionExportedInviteEdit
            ChannelAdminLogEventActionExportedInviteRevoke
            ChannelAdminLogEventActionParticipantInvite
            ChannelAdminLogEventActionParticipantJoin
            ChannelAdminLogEventActionParticipantJoinByInvite
            ChannelAdminLogEventActionParticipantJoinByRequest
            ChannelAdminLogEventActionParticipantLeave
            ChannelAdminLogEventActionParticipantMute
            ChannelAdminLogEventActionParticipantToggleAdmin
            ChannelAdminLogEventActionParticipantToggleBan
            ChannelAdminLogEventActionParticipantUnmute
            ChannelAdminLogEventActionParticipantVolume
            ChannelAdminLogEventActionPinTopic
            ChannelAdminLogEventActionSendMessage
            ChannelAdminLogEventActionStartGroupCall
            ChannelAdminLogEventActionStopPoll
            ChannelAdminLogEventActionToggleAntiSpam
            ChannelAdminLogEventActionToggleForum
            ChannelAdminLogEventActionToggleGroupCallSetting
            ChannelAdminLogEventActionToggleInvites
            ChannelAdminLogEventActionToggleNoForwards
            ChannelAdminLogEventActionTogglePreHistoryHidden
            ChannelAdminLogEventActionToggleSignatures
            ChannelAdminLogEventActionToggleSlowMode
            ChannelAdminLogEventActionUpdatePinned
    """

    QUALNAME = "Octra.raw.base.ChannelAdminLogEventAction"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.Octra.org/telegram/base/channel-admin-log-event-action")
