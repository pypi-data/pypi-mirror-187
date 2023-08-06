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


class SeeOther(RPCError):
    """See Other"""
    CODE = 303
    """``int``: RPC Error Code"""
    NAME = __doc__


class FileMigrate(SeeOther):
    """The file to be accessed is currently stored in DC{value}"""
    ID = "FILE_MIGRATE_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NetworkMigrate(SeeOther):
    """The source IP address is associated with DC{value} (for registration)"""
    ID = "NETWORK_MIGRATE_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhoneMigrate(SeeOther):
    """The phone number a user is trying to use for authorization is associated with DC{value}"""
    ID = "PHONE_MIGRATE_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StatsMigrate(SeeOther):
    """The statistics of the group/channel are stored in DC{value}"""
    ID = "STATS_MIGRATE_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserMigrate(SeeOther):
    """The user whose identity is being used to execute queries is associated with DC{value} (for registration)"""
    ID = "USER_MIGRATE_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


