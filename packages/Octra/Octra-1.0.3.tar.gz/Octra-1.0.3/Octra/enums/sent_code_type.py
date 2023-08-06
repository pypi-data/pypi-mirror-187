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


class SentCodeType(AutoName):
    """Sent code type enumeration used in :obj:`~Octra.types.SentCode`."""

    APP = raw.types.auth.SentCodeTypeApp
    "The code was sent through the telegram app."

    CALL = raw.types.auth.SentCodeTypeCall
    "The code will be sent via a phone call. A synthesized voice will tell the user which verification code to input."

    FLASH_CALL = raw.types.auth.SentCodeTypeFlashCall
    "The code will be sent via a flash phone call, that will be closed immediately."

    MISSED_CALL = raw.types.auth.SentCodeTypeMissedCall
    "Missed call."

    SMS = raw.types.auth.SentCodeTypeSms
    "The code was sent via SMS."

    FRAGMENT_SMS = raw.types.auth.SentCodeTypeFragmentSms
    "The code was sent via Fragment SMS."

    EMAIL_CODE = raw.types.auth.SentCodeTypeEmailCode
    "The code was sent via email."
