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

import Octra
from Octra.handlers import DisconnectHandler
from Octra.handlers.handler import Handler


class AddHandler:
    def add_handler(
        self: "Octra.Client",
        handler: "Handler",
        group: int = 0
    ):
        """Register an update handler.

        You can register multiple handlers, but at most one handler within a group will be used for a single update.
        To handle the same update more than once, register your handler using a different group id (lower group id
        == higher priority). This mechanism is explained in greater details at
        :doc:`More on Updates <../../topics/more-on-updates>`.

        Parameters:
            handler (``Handler``):
                The handler to be registered.

            group (``int``, *optional*):
                The group identifier, defaults to 0.

        Returns:
            ``tuple``: A tuple consisting of *(handler, group)*.

        Example:
            .. code-block:: python

                from Octra import Veteran
                from Octra.handlers import MessageHandler

                async def hello(client, message):
                    print(message)

                app = Client("my_account")

                app.add_handler(MessageHandler(hello))

                app.run()
        """
        if isinstance(handler, DisconnectHandler):
            self.disconnect_handler = handler.callback
        else:
            self.dispatcher.add_handler(handler, group)

        return handler, group
