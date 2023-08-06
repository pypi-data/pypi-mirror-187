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

from Octra import raw, enums
from ..object import Object


class SentCode(Object):
    """Contains info on a sent confirmation code.

    Parameters:
        type (:obj:`~Octra.enums.SentCodeType`):
            Type of the current sent code.

        phone_code_hash (``str``):
            Confirmation code identifier useful for the next authorization steps (either
            :meth:`~Octra.Client.sign_in` or :meth:`~Octra.Client.sign_up`).

        next_type (:obj:`~Octra.enums.NextCodeType`, *optional*):
            Type of the next code to be sent with :meth:`~Octra.Client.resend_code`.

        timeout (``int``, *optional*):
            Delay in seconds before calling :meth:`~Octra.Client.resend_code`.
    """

    def __init__(
        self, *,
        type: "enums.SentCodeType",
        phone_code_hash: str,
        next_type: "enums.NextCodeType" = None,
        timeout: int = None
    ):
        super().__init__()

        self.type = type
        self.phone_code_hash = phone_code_hash
        self.next_type = next_type
        self.timeout = timeout

    @staticmethod
    def _parse(sent_code: raw.types.auth.SentCode) -> "SentCode":
        return SentCode(
            type=enums.SentCodeType(type(sent_code.type)),
            phone_code_hash=sent_code.phone_code_hash,
            next_type=enums.NextCodeType(type(sent_code.next_type)) if sent_code.next_type else None,
            timeout=sent_code.timeout
        )
