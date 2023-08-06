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

import asyncio
import functools
import inspect
import threading

from Octra import types
from Octra.methods import Methods
from Octra.methods.utilities import idle as idle_module, compose as compose_module


def async_to_sync(obj, name):
    function = getattr(obj, name)
    main_loop = asyncio.get_event_loop()

    def async_to_sync_gen(agen, loop, is_main_thread):
        async def anext(agen):
            try:
                return await agen.__anext__(), False
            except StopAsyncIteration:
                return None, True

        while True:
            if is_main_thread:
                item, done = loop.run_until_complete(anext(agen))
            else:
                item, done = asyncio.run_coroutine_threadsafe(anext(agen), loop).result()

            if done:
                break

            yield item

    @functools.wraps(function)
    def async_to_sync_wrap(*args, **kwargs):
        coroutine = function(*args, **kwargs)

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if threading.current_thread() is threading.main_thread() or not main_loop.is_running():
            if loop.is_running():
                return coroutine
            else:
                if inspect.iscoroutine(coroutine):
                    return loop.run_until_complete(coroutine)

                if inspect.isasyncgen(coroutine):
                    return async_to_sync_gen(coroutine, loop, True)
        else:
            if inspect.iscoroutine(coroutine):
                if loop.is_running():
                    async def coro_wrapper():
                        return await asyncio.wrap_future(asyncio.run_coroutine_threadsafe(coroutine, main_loop))

                    return coro_wrapper()
                else:
                    return asyncio.run_coroutine_threadsafe(coroutine, main_loop).result()

            if inspect.isasyncgen(coroutine):
                if loop.is_running():
                    return coroutine
                else:
                    return async_to_sync_gen(coroutine, main_loop, False)

    setattr(obj, name, async_to_sync_wrap)


def wrap(source):
    for name in dir(source):
        method = getattr
        if not name.startswith("_"):
            if inspect.iscoroutinefunction(method) or inspect.isasyncgenfunction(method):
                async_to_sync(source, name)


# t.me/TheVenomXD Wrap all Client's relevant methods
wrap(Methods)

# t.me/TheVenomXD Wrap types' bound methods
for class_name in dir(types):
    cls = getattr(types, class_name)

    if inspect.isclass(cls):
        wrap(cls)

# t.me/TheVenomXD Special case for idle and compose, because they are not inside Methods
async_to_sync(idle_module, "idle")
idle = getattr(idle_module, "idle")

async_to_sync(compose_module, "compose")
compose = getattr(compose_module, "compose")
