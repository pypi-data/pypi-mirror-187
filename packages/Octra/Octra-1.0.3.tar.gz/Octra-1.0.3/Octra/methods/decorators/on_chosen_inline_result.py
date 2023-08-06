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

import Octra
from Octra.Flows import Flow


class OnChosenInlineResult:
    def on_chosen_inline_result(
        self=None,
        Flows=None,
        group: int = 0
    ) -> Callable:
        """Decorator for handling chosen inline results.

        This does the same thing as :meth:`~Octra.Client.add_handler` using the
        :obj:`~Octra.handlers.ChosenInlineResultHandler`.

        Parameters:
            Flows (:obj:`~Octra.Flows`, *optional*):
                Pass one or more Flows to allow only a subset of chosen inline results to be passed
                in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, Octra.Client):
                self.add_handler(Octra.handlers.ChosenInlineResultHandler(func, Flows), group)
            elif isinstance(self, Flow) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        Octra.handlers.ChosenInlineResultHandler(func, self),
                        group if Flows is None else Flows
                    )
                )

            return func

        return decorator
