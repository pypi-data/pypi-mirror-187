# t.me/TheVenomXD Octra - Telegram MTProto API Client Library for Python
# t.me/TheVenomXD Copyright (C) 2017-present Akash <https://github.com/DesiNobita>
# t.me/TheVenomXD
# t.me/TheVenomXD This file is part of Octra.
# t.me/TheVenomXD
# t.me/TheVenomXD Octra is free software: you can redistribute it and/or modify
# t.me/TheVenomXD it under the terms of the GNU Lesser General Public License as published
# t.me/TheVenomXD by the Free Software Foundation, either version 3 of the License, or
# t.me/TheVenomXD (at your option) any later version.
# t.me/TheVenomXD
# t.me/TheVenomXD Octra is distributed in the hope that it will be useful,
# t.me/TheVenomXD but WITHOUT ANY WARRANTY; without even the implied warranty of
# t.me/TheVenomXD MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# t.me/TheVenomXD GNU Lesser General Public License for more details.
# t.me/TheVenomXD
# t.me/TheVenomXD You should have received a copy of the GNU Lesser General Public License
# t.me/TheVenomXD along with Octra.  If not, see <http://www.gnu.org/licenses/>.

from ..rpc_error import RPCError


class NotAcceptable(RPCError):
    """Not Acceptable"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = __doc__


class OctraAuthKeyDuplicated(NotAcceptable):
    """The same authorization key (session file) was used in more than one place simultaneously. You must delete your session file and log in again with your phone number or bot token"""
    ID = "octra_auth_key_DUPLICATED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChannelPrivate(NotAcceptable):
    """The channel/supergroup is not accessible"""
    ID = "CHANNEL_PRIVATE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FilerefUpgradeNeeded(NotAcceptable):
    """The file reference has expired and you must use a refreshed one by obtaining the original media message"""
    ID = "FILEREF_UPGRADE_NEEDED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FreshChangeAdminsForbidden(NotAcceptable):
    """You were just elected admin, you can't add or modify other admins yet"""
    ID = "FRESH_CHANGE_ADMINS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FreshChangePhoneForbidden(NotAcceptable):
    """You can't change your phone number because your session was logged-in recently"""
    ID = "FRESH_CHANGE_PHONE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FreshResetAuthorisationForbidden(NotAcceptable):
    """You can't terminate other authorized sessions because the current was logged-in recently"""
    ID = "FRESH_RESET_AUTHORISATION_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhoneNumberInvalid(NotAcceptable):
    """The phone number is invalid"""
    ID = "PHONE_NUMBER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhonePasswordFlood(NotAcceptable):
    """You have tried to log-in too many times"""
    ID = "PHONE_PASSWORD_FLOOD"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickersetInvalid(NotAcceptable):
    """The sticker set is invalid"""
    ID = "STICKERSET_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickersetOwnerAnonymous(NotAcceptable):
    """This sticker set can't be used as the group's sticker set because it was created by one of its anonymous admins"""
    ID = "STICKERSET_OWNER_ANONYMOUS"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserpicUploadRequired(NotAcceptable):
    """You must have a profile picture to publish your geolocation"""
    ID = "USERPIC_UPLOAD_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserRestricted(NotAcceptable):
    """You are limited/restricted. You can't perform this action"""
    ID = "USER_RESTRICTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


