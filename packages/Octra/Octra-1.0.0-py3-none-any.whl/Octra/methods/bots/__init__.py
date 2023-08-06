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

from .answer_callback_query import AnswerCallbackQuery
from .answer_inline_query import AnswerInlineQuery
from .answer_web_app_query import AnswerWebAppQuery
from .delete_bot_commands import DeleteBotCommands
from .get_bot_commands import ExtractBotCommands
from .get_bot_default_privileges import ExtractBotDefaultPrivileges
from .get_chat_menu_button import ExtractChatMenuButton
from .get_game_high_scores import ExtractGameHighScores
from .get_inline_bot_results import ExtractInlineBotResults
from .request_callback_answer import RequestCallbackAnswer
from .send_game import SendGame
from .send_inline_bot_result import SendInlineBotResult
from .set_bot_commands import SetBotCommands
from .set_bot_default_privileges import SetBotDefaultPrivileges
from .set_chat_menu_button import SetChatMenuButton
from .set_game_score import SetGameScore


class Bots(
    AnswerCallbackQuery,
    AnswerInlineQuery,
    ExtractInlineBotResults,
    RequestCallbackAnswer,
    SendInlineBotResult,
    SendGame,
    SetGameScore,
    ExtractGameHighScores,
    SetBotCommands,
    ExtractBotCommands,
    DeleteBotCommands,
    SetBotDefaultPrivileges,
    ExtractBotDefaultPrivileges,
    SetChatMenuButton,
    ExtractChatMenuButton,
    AnswerWebAppQuery
):
    pass
