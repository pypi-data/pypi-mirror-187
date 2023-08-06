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

from Octra import raw, utils
from ..object import Object


class SentWebAppMessage(Object):
    """Contains information about an inline message sent by a `Web App <https://core.telegram.org/bots/webapps>`_ on behalf of a user.

    Parameters:
        inline_message_id (``str``):
            Identifier of the sent inline message.
            Available only if there is an inline keyboard attached to the message.
    """

    def __init__(
        self, *,
        inline_message_id: str,
    ):
        super().__init__()

        self.inline_message_id = inline_message_id

    @staticmethod
    def _parse(obj: "raw.types.WebViewMessageSent"):
        return SentWebAppMessage(inline_message_id=utils.pack_inline_message_id(obj.msg_id))
