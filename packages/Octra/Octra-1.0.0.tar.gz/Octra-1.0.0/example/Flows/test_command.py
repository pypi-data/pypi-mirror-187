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

import pytest

from Octra import Flows
from example.flows import Client, Message

c = Client()


@pytest.mark.asyncio
async def test_single():
    f = Flows.command("start")

    m = Message("/start")
    assert await f(c, m)


@pytest.mark.asyncio
async def test_multiple():
    f = Flows.command(["start", "help"])

    m = Message("/start")
    assert await f(c, m)

    m = Message("/help")
    assert await f(c, m)

    m = Message("/settings")
    assert not await f(c, m)


@pytest.mark.asyncio
async def test_prefixes():
    f = Flows.command("start", prefixes=list(".!# t.me/TheVenomXD"))

    m = Message(".start")
    assert await f(c, m)

    m = Message("!start")
    assert await f(c, m)

    m = Message("# t.me/TheVenomXDstart")
    assert await f(c, m)

    m = Message("/start")
    assert not await f(c, m)


@pytest.mark.asyncio
async def test_case_sensitive():
    f = Flows.command("start", case_sensitive=True)

    m = Message("/start")
    assert await f(c, m)

    m = Message("/StArT")
    assert not await f(c, m)


@pytest.mark.asyncio
async def test_case_insensitive():
    f = Flows.command("start", case_sensitive=False)

    m = Message("/start")
    assert await f(c, m)

    m = Message("/StArT")
    assert await f(c, m)


@pytest.mark.asyncio
async def test_with_mention():
    f = Flows.command("start")

    m = Message("/start@username")
    assert await f(c, m)

    m = Message("/start@UserName")
    assert await f(c, m)

    m = Message("/start@another")
    assert not await f(c, m)


@pytest.mark.asyncio
async def test_with_args():
    f = Flows.command("start")

    m = Message("/start")
    await f(c, m)
    assert m.command == ["start"]

    m = Message("/StArT")
    await f(c, m)
    assert m.command == ["start"]

    m = Message("/start@username")
    await f(c, m)
    assert m.command == ["start"]

    m = Message("/start a b c")
    await f(c, m)
    assert m.command == ["start"] + list("abc")

    m = Message('/start@username a b c')
    await f(c, m)
    assert m.command == ["start"] + list("abc")

    m = Message("/start 'a b' c")
    await f(c, m)
    assert m.command == ["start", "a b", "c"]

    m = Message('/start     a     b     "c     d"')
    await f(c, m)
    assert m.command == ["start"] + list("ab") + ["c     d"]


@pytest.mark.asyncio
async def test_caption():
    f = Flows.command("start")

    m = Message(caption="/start")
    assert await f(c, m)


@pytest.mark.asyncio
async def test_no_text():
    f = Flows.command("start")

    m = Message()
    assert not await f(c, m)
