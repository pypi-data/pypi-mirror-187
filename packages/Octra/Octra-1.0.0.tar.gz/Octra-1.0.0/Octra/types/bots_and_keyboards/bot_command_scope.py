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
from ..object import Object


class BotCommandScope(Object):
    """Represents the scope to which bot commands are applied.

    Currently, the following 7 scopes are supported:

    - :obj:`~Octra.types.BotCommandScopeDefault`
    - :obj:`~Octra.types.BotCommandScopeAllPrivateChats`
    - :obj:`~Octra.types.BotCommandScopeAllGroupChats`
    - :obj:`~Octra.types.BotCommandScopeAllChatAdministrators`
    - :obj:`~Octra.types.BotCommandScopeChat`
    - :obj:`~Octra.types.BotCommandScopeChatAdministrators`
    - :obj:`~Octra.types.BotCommandScopeChatUSER`

    **Determining list of commands**

    The following algorithm is used to determine the list of commands for a particular user viewing the bot menu.
    The first list of commands which is set is returned:

    **Commands in the chat with the bot**:

    - BotCommandScopeChat + language_code
    - BotCommandScopeChat
    - BotCommandScopeAllPrivateChats + language_code
    - BotCommandScopeAllPrivateChats
    - BotCommandScopeDefault + language_code
    - BotCommandScopeDefault

    **Commands in group and supergroup chats**

    - BotCommandScopeChatUSER + language_code
    - BotCommandScopeChatUSER
    - BotCommandScopeChatAdministrators + language_code (administrators only)
    - BotCommandScopeChatAdministrators (administrators only)
    - BotCommandScopeChat + language_code
    - BotCommandScopeChat
    - BotCommandScopeAllChatAdministrators + language_code (administrators only)
    - BotCommandScopeAllChatAdministrators (administrators only)
    - BotCommandScopeAllGroupChats + language_code
    - BotCommandScopeAllGroupChats
    - BotCommandScopeDefault + language_code
    - BotCommandScopeDefault
    """

    def __init__(self, type: str):
        super().__init__()

        self.type = type

    async def write(self, client: "Octra.Client") -> "raw.base.BotCommandScope":
        raise NotImplementedError
