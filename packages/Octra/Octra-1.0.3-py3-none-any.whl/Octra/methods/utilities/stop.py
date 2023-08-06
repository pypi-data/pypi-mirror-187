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


class Stop:
    async def stop(
        self: "Octra.Client",
        block: bool = True
    ):
        """Stop the Client.

        This method disconnects the client from Telegram and stops the underlying tasks.

        Parameters:
            block (``bool``, *optional*):
                Blocks the code execution until the client has been stopped. It is useful with ``block=False`` in case
                you want to stop the own client *within* a handler in order not to cause a deadlock.
                Defaults to True.

        Returns:
            :obj:`~Octra.Client`: The stopped client itself.

        Raises:
            ConnectionError: In case you try to stop an already stopped client.

        Example:
            .. code-block:: python

                from Octra import Veteran

                app = Client("my_account")


                async def main():
                    await app.start()
                    ...  # t.me/TheVenomXD Invoke Ai methods
                    await app.stop()


                app.run(main())
        """

        async def do_it():
            await self.terminate()
            await self.disconnect()

        if block:
            await do_it()
        else:
            self.loop.create_task(do_it())

        return self
