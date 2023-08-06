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

import Octra
from Octra import raw
from Octra import types


class AnswerWebAppQuery:
    async def answer_web_app_query(
        self: "Octra.Client",
        web_app_query_id: str,
        result: "types.InlineQueryResult"
    ) -> "types.SentWebAppMessage":
        """Set the result of an interaction with a `Web App <https://core.telegram.org/bots/webapps>`_ and send a
        corresponding message on behalf of the user to the chat from which the query originated.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            web_app_query_id (``str``):
                Unique identifier for the answered query.

            result (:obj:`~Octra.types.InlineQueryResult`):
                A list of results for the inline query.

        Returns:
            :obj:`~Octra.types.SentWebAppMessage`: On success the sent web app message is returned.
        """

        r = await self.invoke(
            raw.functions.messages.SendWebViewResultMessage(
                bot_query_id=web_app_query_id,
                result=await result.write(self)
            )
        )

        return types.SentWebAppMessage._parse(r)
