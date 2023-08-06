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


class Unauthorized(RPCError):
    """Unauthorized"""
    CODE = 401
    """``int``: RPC Error Code"""
    NAME = __doc__


class ActiveUserRequired(Unauthorized):
    """The method is only available to already activated users"""
    ID = "ACTIVE_USER_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class OctraAuthKeyInvalid(Unauthorized):
    """The key is invalid"""
    ID = "octra_auth_key_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class OctraAuthKeyPermEmpty(Unauthorized):
    """The method is unavailable for temporary authorization key, not bound to permanent"""
    ID = "octra_auth_key_PERM_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class OctraAuthKeyUnregistered(Unauthorized):
    """The key is not registered in the system. Delete your session file and login again"""
    ID = "octra_auth_key_UNREGISTERED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SessionExpired(Unauthorized):
    """The authorization has expired"""
    ID = "SESSION_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SessionPasswordNeeded(Unauthorized):
    """The two-step verification is enabled and a password is required"""
    ID = "SESSION_PASSWORD_NEEDED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SessionRevoked(Unauthorized):
    """The authorization has been invalidated, because of the user terminating all sessions"""
    ID = "SESSION_REVOKED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserDeactivated(Unauthorized):
    """The user has been deleted/deactivated"""
    ID = "USER_DEACTIVATED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserDeactivatedBan(Unauthorized):
    """The user has been deleted/deactivated"""
    ID = "USER_DEACTIVATED_BAN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


