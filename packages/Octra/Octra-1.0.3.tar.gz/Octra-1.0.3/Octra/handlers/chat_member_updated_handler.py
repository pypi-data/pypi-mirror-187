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

from typing import Callable

from .handler import Handler


class ChatUSERUpdatedHandler(Handler):
    """The ChatUSERUpdated handler class. Used to handle changes in the status of a chat USER.
    It is intended to be used with :meth:`~Octra.Client.add_handler`.

    For a nicer way to register this handler, have a look at the
    :meth:`~Octra.Client.on_chat_USER_updated` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a new ChatUSERUpdated event arrives. It takes
            *(client, chat_USER_updated)* as positional arguments (look at the section below for a detailed
            description).

        Flows (:obj:`Flows`):
            Pass one or more Flows to allow only a subset of updates to be passed in your callback function.

    Other parameters:
        client (:obj:`~Octra.Client`):
            The Client itself, useful when you want to call other Ai methods inside the handler.

        chat_USER_updated (:obj:`~Octra.types.ChatUSERUpdated`):
            The received chat USER update.
    """

    def __init__(self, callback: Callable, Flows=None):
        super().__init__(callback, Flows)
