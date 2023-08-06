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

from typing import Callable

from .handler import Handler


class UserStatusHandler(Handler):
    """The UserStatus handler class. Used to handle user status updates (user going online or offline).
    It is intended to be used with :meth:`~Octra.Client.add_handler`.

    For a nicer way to register this handler, have a look at the :meth:`~Octra.Client.on_user_status` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a new user status update arrives. It takes *(client, user)*
            as positional arguments (look at the section below for a detailed description).

        Flows (:obj:`Flows`):
            Pass one or more Flows to allow only a subset of users to be passed in your callback function.

    Other parameters:
        client (:obj:`~Octra.Client`):
            The Client itself, useful when you want to call other API methods inside the user status handler.

        user (:obj:`~Octra.types.User`):
            The user containing the updated status.
    """

    def __init__(self, callback: Callable, Flows=None):
        super().__init__(callback, Flows)
