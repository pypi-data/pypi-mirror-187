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


class Flood(RPCError):
    """Flood"""
    CODE = 420
    """``int``: RPC Error Code"""
    NAME = __doc__


class TwoFaConfirmWait(Flood):
    """A wait of {value} seconds is required because this account is active and protected by a 2FA password"""
    ID = "2FA_CONFIRM_WAIT_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FloodTestPhoneWait(Flood):
    """A wait of {value} seconds is required in the test servers"""
    ID = "FLOOD_TEST_PHONE_WAIT_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FloodWait(Flood):
    """A wait of {value} seconds is required"""
    ID = "FLOOD_WAIT_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SlowmodeWait(Flood):
    """A wait of {value} seconds is required to send messages in this chat."""
    ID = "SLOWMODE_WAIT_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TakeoutInitDelay(Flood):
    """You have to confirm the data export request using one of your mobile devices or wait {value} seconds"""
    ID = "TAKEOUT_INIT_DELAY_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


