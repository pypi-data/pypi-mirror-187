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

import inspect
from typing import Callable

import Octra
from Octra.Flows import Flow
from Octra.types import Update


class Handler:
    def __init__(self, callback: Callable, Flows: Flow = None):
        self.callback = callback
        self.Flows = Flows

    async def check(self, client: "Octra.Client", update: Update):
        if callable(self.Flows):
            if inspect.iscoroutinefunction(self.Flows.__call__):
                return await self.Flows(client, update)
            else:
                return await client.loop.run_in_executor(
                    client.executor,
                    self.Flows,
                    client, update
                )

        return True
