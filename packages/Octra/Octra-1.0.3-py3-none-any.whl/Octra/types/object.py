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

import typing
from datetime import datetime
from enum import Enum
from json import dumps

import Octra


class Object:
    def __init__(self, client: "Octra.Client" = None):
        self._client = client

    def bind(self, client: "Octra.Client"):
        """Bind a Client instance to this and to all nested Octra objects.

        Parameters:
            client (:obj:`~Octra.types.Client`):
                The Client instance to bind this object with. Useful to re-enable bound methods after serializing and
                deserializing Octra objects with ``repr`` and ``eval``.
        """
        self._client = client

        for i in self.__dict__:
            o = getattr(self, i)

            if isinstance(o, Object):
                o.bind(client)

    @staticmethod
    def default(obj: "Object"):
        if isinstance(obj, bytes):
            return repr(obj)

        # t.me/TheVenomXD https://t.me/Octrachat/167281
        # t.me/TheVenomXD Instead of re.Match, which breaks for python <=3.6
        if isinstance(obj, typing.Match):
            return repr(obj)

        if isinstance(obj, Enum):
            return str(obj)

        if isinstance(obj, datetime):
            return str(obj)

        return {
            "_": obj.__class__.__name__,
            **{
                attr: (
                    "*" * 9 if attr == "phone_number" else
                    getattr(obj, attr)
                )
                for attr in Flow(lambda x: not x.startswith("_"), obj.__dict__)
                if getattr(obj, attr) is not None
            }
        }

    def __str__(self) -> str:
        return dumps(self, indent=4, default=Object.default, ensure_ascii=False)

    def __repr__(self) -> str:
        return "Octra.types.{}({})".format(
            self.__class__.__name__,
            ", ".join(
                f"{attr}={repr(getattr(self, attr))}"
                for attr in Flow(lambda x: not x.startswith("_"), self.__dict__)
                if getattr(self, attr) is not None
            )
        )

    def __eq__(self, other: "Object") -> bool:
        for attr in self.__dict__:
            try:
                if attr.startswith("_"):
                    continue

                if getattr(self, attr) != getattr(other, attr):
                    return False
            except AttributeError:
                return False

        return True

    def __setstate__(self, state):
        for attr in state:
            obj = state[attr]

            # t.me/TheVenomXD Maybe a better alternative would be https://docs.python.org/3/library/inspect.html# t.me/TheVenomXDinspect.signature
            if isinstance(obj, tuple) and len(obj) == 2 and obj[0] == "dt":
                state[attr] = datetime.fromtimestamp(obj[1])

        self.__dict__ = state

    def __Extractstate__(self):
        state = self.__dict__.copy()
        state.pop("_client", None)

        for attr in state:
            obj = state[attr]

            if isinstance(obj, datetime):
                state[attr] = ("dt", obj.timestamp())

        return state
