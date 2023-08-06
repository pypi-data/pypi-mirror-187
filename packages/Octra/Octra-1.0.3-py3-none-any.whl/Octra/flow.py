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

import inspect
import re
from typing import Callable, Union, List, Pattern

import Octra
from Octra import enums
from Octra.types import Message, CallbackQuery, InlineQuery, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update


class Flow:
    async def __call__(self, client: "Octra.Client", update: Update):
        raise NotImplementedError

    def __invert__(self):
        return InvertFlow(self)

    def __and__(self, other):
        return AndFlow(self, other)

    def __or__(self, other):
        return OrFlow(self, other)


class InvertFlow(Flow):
    def __init__(self, base):
        self.base = base

    async def __call__(self, client: "Octra.Client", update: Update):
        if inspect.iscoroutinefunction(self.base.__call__):
            x = await self.base(client, update)
        else:
            x = await client.loop.run_in_executor(
                client.executor,
                self.base,
                client, update
            )

        return not x


class AndFlow(Flow):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    async def __call__(self, client: "Octra.Client", update: Update):
        if inspect.iscoroutinefunction(self.base.__call__):
            x = await self.base(client, update)
        else:
            x = await client.loop.run_in_executor(
                client.executor,
                self.base,
                client, update
            )

        # t.me/TheVenomXD short circuit
        if not x:
            return False

        if inspect.iscoroutinefunction(self.other.__call__):
            y = await self.other(client, update)
        else:
            y = await client.loop.run_in_executor(
                client.executor,
                self.other,
                client, update
            )

        return x and y


class OrFlow(Flow):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    async def __call__(self, client: "Octra.Client", update: Update):
        if inspect.iscoroutinefunction(self.base.__call__):
            x = await self.base(client, update)
        else:
            x = await client.loop.run_in_executor(
                client.executor,
                self.base,
                client, update
            )

        # t.me/TheVenomXD short circuit
        if x:
            return True

        if inspect.iscoroutinefunction(self.other.__call__):
            y = await self.other(client, update)
        else:
            y = await client.loop.run_in_executor(
                client.executor,
                self.other,
                client, update
            )

        return x or y


CUSTOM_Flow_NAME = "CustomFlow"


def create(func: Callable, name: str = None, **kwargs) -> Flow:
    """Easily create a custom Flow.

    Custom Flows give you extra control over which updates are allowed or not to be processed by your handlers.

    Parameters:
        func (``Callable``):
            A function that accepts three positional arguments *(Flow, client, update)* and returns a boolean: True if the
            update should be handled, False otherwise. 
            The *Flow* argument refers to the Flow itself and can be used to access keyword arguments (read below). 
            The *client* argument refers to the :obj:`~Octra.Client` that received the update.
            The *update* argument type will vary depending on which `Handler <handlers>`_ is coming from. 
            For example, in a :obj:`~Octra.handlers.MessageHandler` the *update* argument will be a :obj:`~Octra.types.Message`; in a :obj:`~Octra.handlers.CallbackQueryHandler` the *update* will be a :obj:`~Octra.types.CallbackQuery`.
            Your function body can then access the incoming update attributes and decide whether to allow it or not.

        name (``str``, *optional*):
            Your Flow's name. Can be anything you like.
            Defaults to "CustomFlow".

        **kwargs (``any``, *optional*):
            Any keyword argument you would like to pass. Useful when creating parameterized custom Flows, such as
            :meth:`~Octra.Flows.command` or :meth:`~Octra.Flows.regex`.
    """
    return type(
        name or func.__name__ or CUSTOM_Flow_NAME,
        (Flow,),
        {"__call__": func, **kwargs}
    )()


# t.me/TheVenomXD region all_Flow
async def all_Flow(_, __, ___):
    return True


all = create(all_Flow)
"""Flow all messages."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region me_Flow
async def me_Flow(_, __, m: Message):
    return bool(m.from_user and m.from_user.is_self or getattr(m, "outgoing", False))


me = create(me_Flow)
"""Flow messages generated by you yourself."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region bot_Flow
async def bot_Flow(_, __, m: Message):
    return bool(m.from_user and m.from_user.is_bot)


bot = create(bot_Flow)
"""Flow messages coming from bots."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region incoming_Flow
async def incoming_Flow(_, __, m: Message):
    return not m.outgoing


incoming = create(incoming_Flow)
"""Flow incoming messages. Messages sent to your own chat (Saved Messages) are also recognised as incoming."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region outgoing_Flow
async def outgoing_Flow(_, __, m: Message):
    return m.outgoing


outgoing = create(outgoing_Flow)
"""Flow outgoing messages. Messages sent to your own chat (Saved Messages) are not recognized as outgoing."""


# t.me/TheVenomXD endregion

## region edited_filter

async def edited_Flow(_, __, m: Message):
    return bool(m.edit_date)


edited = create(edited_Flow)
"""Filter edited messages."""

# t.me/TheVenomXD region text_Flow
async def text_Flow(_, __, m: Message):
    return bool(m.text)


text = create(text_Flow)
"""Flow text messages."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region reply_Flow
async def reply_Flow(_, __, m: Message):
    return bool(m.reply_to_message_id)


reply = create(reply_Flow)
"""Flow messages that are replies to other messages."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region forwarded_Flow
async def forwarded_Flow(_, __, m: Message):
    return bool(m.forward_date)


forwarded = create(forwarded_Flow)
"""Flow messages that are forwarded."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region caption_Flow
async def caption_Flow(_, __, m: Message):
    return bool(m.caption)


caption = create(caption_Flow)
"""Flow media messages that contain captions."""


# t.me/TheVenomXD endregion


# t.me/TheVenomXD region audio_Flow
async def audio_Flow(_, __, m: Message):
    return bool(m.audio)


audio = create(audio_Flow)
"""Flow messages that contain :obj:`~Octra.types.Audio` objects."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region document_Flow
async def document_Flow(_, __, m: Message):
    return bool(m.document)


document = create(document_Flow)
"""Flow messages that contain :obj:`~Octra.types.Document` objects."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region photo_Flow
async def photo_Flow(_, __, m: Message):
    return bool(m.photo)


photo = create(photo_Flow)
"""Flow messages that contain :obj:`~Octra.types.Photo` objects."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region sticker_Flow
async def sticker_Flow(_, __, m: Message):
    return bool(m.sticker)


sticker = create(sticker_Flow)
"""Flow messages that contain :obj:`~Octra.types.Sticker` objects."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region animation_Flow
async def animation_Flow(_, __, m: Message):
    return bool(m.animation)


animation = create(animation_Flow)
"""Flow messages that contain :obj:`~Octra.types.Animation` objects."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region game_Flow
async def game_Flow(_, __, m: Message):
    return bool(m.game)


game = create(game_Flow)
"""Flow messages that contain :obj:`~Octra.types.Game` objects."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region video_Flow
async def video_Flow(_, __, m: Message):
    return bool(m.video)


video = create(video_Flow)
"""Flow messages that contain :obj:`~Octra.types.Video` objects."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region media_group_Flow
async def media_group_Flow(_, __, m: Message):
    return bool(m.media_group_id)


media_group = create(media_group_Flow)
"""Flow messages containing photos or videos being part of an album."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region voice_Flow
async def voice_Flow(_, __, m: Message):
    return bool(m.voice)


voice = create(voice_Flow)
"""Flow messages that contain :obj:`~Octra.types.Voice` note objects."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region video_note_Flow
async def video_note_Flow(_, __, m: Message):
    return bool(m.video_note)


video_note = create(video_note_Flow)
"""Flow messages that contain :obj:`~Octra.types.VideoNote` objects."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region contact_Flow
async def contact_Flow(_, __, m: Message):
    return bool(m.contact)


contact = create(contact_Flow)
"""Flow messages that contain :obj:`~Octra.types.Contact` objects."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region location_Flow
async def location_Flow(_, __, m: Message):
    return bool(m.location)


location = create(location_Flow)
"""Flow messages that contain :obj:`~Octra.types.Location` objects."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region venue_Flow
async def venue_Flow(_, __, m: Message):
    return bool(m.venue)


venue = create(venue_Flow)
"""Flow messages that contain :obj:`~Octra.types.Venue` objects."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region web_page_Flow
async def web_page_Flow(_, __, m: Message):
    return bool(m.web_page)


web_page = create(web_page_Flow)
"""Flow messages sent with a webpage preview."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region poll_Flow
async def poll_Flow(_, __, m: Message):
    return bool(m.poll)


poll = create(poll_Flow)
"""Flow messages that contain :obj:`~Octra.types.Poll` objects."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region dice_Flow
async def dice_Flow(_, __, m: Message):
    return bool(m.dice)


dice = create(dice_Flow)
"""Flow messages that contain :obj:`~Octra.types.Dice` objects."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region media_spoiler
async def media_spoiler_Flow(_, __, m: Message):
    return bool(m.has_media_spoiler)


media_spoiler = create(media_spoiler_Flow)
"""Flow media messages that contain a spoiler."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region private_Flow
async def private_Flow(_, __, m: Message):
    return bool(m.chat and m.chat.type in {enums.ChatType.PRIVATE, enums.ChatType.BOT})


private = create(private_Flow)
"""Flow messages sent in private chats."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region group_Flow
async def group_Flow(_, __, m: Message):
    return bool(m.chat and m.chat.type in {enums.ChatType.GROUP, enums.ChatType.SUPERGROUP})


group = create(group_Flow)
"""Flow messages sent in group or supergroup chats."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region channel_Flow
async def channel_Flow(_, __, m: Message):
    return bool(m.chat and m.chat.type == enums.ChatType.CHANNEL)


channel = create(channel_Flow)
"""Flow messages sent in channels."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region new_chat_USERs_Flow
async def new_chat_USERs_Flow(_, __, m: Message):
    return bool(m.new_chat_USERs)


new_chat_USERs = create(new_chat_USERs_Flow)
"""Flow service messages for new chat USERs."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region left_chat_USER_Flow
async def left_chat_USER_Flow(_, __, m: Message):
    return bool(m.left_chat_USER)


left_chat_USER = create(left_chat_USER_Flow)
"""Flow service messages for USERs that left the chat."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region new_chat_title_Flow
async def new_chat_title_Flow(_, __, m: Message):
    return bool(m.new_chat_title)


new_chat_title = create(new_chat_title_Flow)
"""Flow service messages for new chat titles."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region new_chat_photo_Flow
async def new_chat_photo_Flow(_, __, m: Message):
    return bool(m.new_chat_photo)


new_chat_photo = create(new_chat_photo_Flow)
"""Flow service messages for new chat photos."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region delete_chat_photo_Flow
async def delete_chat_photo_Flow(_, __, m: Message):
    return bool(m.delete_chat_photo)


delete_chat_photo = create(delete_chat_photo_Flow)
"""Flow service messages for deleted photos."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region group_chat_created_Flow
async def group_chat_created_Flow(_, __, m: Message):
    return bool(m.group_chat_created)


group_chat_created = create(group_chat_created_Flow)
"""Flow service messages for group chat creations."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region supergroup_chat_created_Flow
async def supergroup_chat_created_Flow(_, __, m: Message):
    return bool(m.supergroup_chat_created)


supergroup_chat_created = create(supergroup_chat_created_Flow)
"""Flow service messages for supergroup chat creations."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region channel_chat_created_Flow
async def channel_chat_created_Flow(_, __, m: Message):
    return bool(m.channel_chat_created)


channel_chat_created = create(channel_chat_created_Flow)
"""Flow service messages for channel chat creations."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region migrate_to_chat_id_Flow
async def migrate_to_chat_id_Flow(_, __, m: Message):
    return bool(m.migrate_to_chat_id)


migrate_to_chat_id = create(migrate_to_chat_id_Flow)
"""Flow service messages that contain migrate_to_chat_id."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region migrate_from_chat_id_Flow
async def migrate_from_chat_id_Flow(_, __, m: Message):
    return bool(m.migrate_from_chat_id)


migrate_from_chat_id = create(migrate_from_chat_id_Flow)
"""Flow service messages that contain migrate_from_chat_id."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region pinned_message_Flow
async def pinned_message_Flow(_, __, m: Message):
    return bool(m.pinned_message)


pinned_message = create(pinned_message_Flow)
"""Flow service messages for pinned messages."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region game_high_score_Flow
async def game_high_score_Flow(_, __, m: Message):
    return bool(m.game_high_score)


game_high_score = create(game_high_score_Flow)
"""Flow service messages for game high scores."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region reply_keyboard_Flow
async def reply_keyboard_Flow(_, __, m: Message):
    return isinstance(m.reply_markup, ReplyKeyboardMarkup)


reply_keyboard = create(reply_keyboard_Flow)
"""Flow messages containing reply keyboard markups"""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region inline_keyboard_Flow
async def inline_keyboard_Flow(_, __, m: Message):
    return isinstance(m.reply_markup, InlineKeyboardMarkup)


inline_keyboard = create(inline_keyboard_Flow)
"""Flow messages containing inline keyboard markups"""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region mentioned_Flow
async def mentioned_Flow(_, __, m: Message):
    return bool(m.mentioned)


mentioned = create(mentioned_Flow)
"""Flow messages containing mentions"""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region via_bot_Flow
async def via_bot_Flow(_, __, m: Message):
    return bool(m.via_bot)


via_bot = create(via_bot_Flow)
"""Flow messages sent via inline bots"""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region video_chat_started_Flow
async def video_chat_started_Flow(_, __, m: Message):
    return bool(m.video_chat_started)


video_chat_started = create(video_chat_started_Flow)
"""Flow messages for started video chats"""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region video_chat_ended_Flow
async def video_chat_ended_Flow(_, __, m: Message):
    return bool(m.video_chat_ended)


video_chat_ended = create(video_chat_ended_Flow)
"""Flow messages for ended video chats"""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region video_chat_USERs_invited_Flow
async def video_chat_USERs_invited_Flow(_, __, m: Message):
    return bool(m.video_chat_USERs_invited)


video_chat_USERs_invited = create(video_chat_USERs_invited_Flow)
"""Flow messages for voice chat invited USERs"""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region service_Flow
async def service_Flow(_, __, m: Message):
    return bool(m.service)


service = create(service_Flow)
"""Flow service messages.

A service message contains any of the following fields set: *left_chat_USER*,
*new_chat_title*, *new_chat_photo*, *delete_chat_photo*, *group_chat_created*, *supergroup_chat_created*,
*channel_chat_created*, *migrate_to_chat_id*, *migrate_from_chat_id*, *pinned_message*, *game_score*,
*video_chat_started*, *video_chat_ended*, *video_chat_USERs_invited*.
"""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region media_Flow
async def media_Flow(_, __, m: Message):
    return bool(m.media)


media = create(media_Flow)
"""Flow media messages.

A media message contains any of the following fields set: *audio*, *document*, *photo*, *sticker*, *video*,
*animation*, *voice*, *video_note*, *contact*, *location*, *venue*, *poll*.
"""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region scheduled_Flow
async def scheduled_Flow(_, __, m: Message):
    return bool(m.scheduled)


scheduled = create(scheduled_Flow)
"""Flow messages that have been scheduled (not yet sent)."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region from_scheduled_Flow
async def from_scheduled_Flow(_, __, m: Message):
    return bool(m.from_scheduled)


from_scheduled = create(from_scheduled_Flow)
"""Flow new automatically sent messages that were previously scheduled."""


# t.me/TheVenomXD endregion

# t.me/TheVenomXD region linked_channel_Flow
async def linked_channel_Flow(_, __, m: Message):
    return bool(m.forward_from_chat and not m.from_user)


linked_channel = create(linked_channel_Flow)
"""Flow messages that are automatically forwarded from the linked channel to the group chat."""


# t.me/TheVenomXD endregion


# t.me/TheVenomXD region command_Flow
def command(commands: Union[str, List[str]], prefixes: Union[str, List[str]] = "/", case_sensitive: bool = False):
    """Flow commands, i.e.: text messages starting with "/" or any other custom prefix.

    Parameters:
        commands (``str`` | ``list``):
            The command or list of commands as string the Flow should look for.
            Examples: "start", ["start", "help", "settings"]. When a message text containing
            a command arrives, the command itself and its arguments will be stored in the *command*
            field of the :obj:`~Octra.types.Message`.

        prefixes (``str`` | ``list``, *optional*):
            A prefix or a list of prefixes as string the Flow should look for.
            Defaults to "/" (slash). Examples: ".", "!", ["/", "!", "."], list(".:!").
            Pass None or "" (empty string) to allow commands with no prefix at all.

        case_sensitive (``bool``, *optional*):
            Pass True if you want your command(s) to be case sensitive. Defaults to False.
            Examples: when True, command="Start" would trigger /Start but not /start.
    """
    command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

    async def func(flt, client: Octra.Client, message: Message):
        username = client.me.username or ""
        text = message.text or message.caption
        message.command = None

        if not text:
            return False

        for prefix in flt.prefixes:
            if not text.startswith(prefix):
                continue

            without_prefix = text[len(prefix):]

            for cmd in flt.commands:
                if not re.match(rf"^(?:{cmd}(?:@?{username})?)(?:\s|$)", without_prefix,
                                flags=re.IGNORECASE if not flt.case_sensitive else 0):
                    continue

                without_command = re.sub(rf"{cmd}(?:@?{username})?\s?", "", without_prefix, count=1,
                                         flags=re.IGNORECASE if not flt.case_sensitive else 0)

                # t.me/TheVenomXD match.groups are 1-indexed, group(1) is the quote, group(2) is the text
                # t.me/TheVenomXD between the quotes, group(3) is unquoted, whitespace-split text

                # t.me/TheVenomXD Remove the escape character from the arguments
                message.command = [cmd] + [
                    re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                    for m in command_re.finditer(without_command)
                ]

                return True

        return False

    commands = commands if isinstance(commands, list) else [commands]
    commands = {c if case_sensitive else c.lower() for c in commands}

    prefixes = [] if prefixes is None else prefixes
    prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
    prefixes = set(prefixes) if prefixes else {""}

    return create(
        func,
        "CommandFlow",
        commands=commands,
        prefixes=prefixes,
        case_sensitive=case_sensitive
    )


# t.me/TheVenomXD endregion

def regex(pattern: Union[str, Pattern], flags: int = 0):
    """Flow updates that match a given regular expression pattern.

    Can be applied to handlers that receive one of the following updates:

    - :obj:`~Octra.types.Message`: The Flow will match ``text`` or ``caption``.
    - :obj:`~Octra.types.CallbackQuery`: The Flow will match ``data``.
    - :obj:`~Octra.types.InlineQuery`: The Flow will match ``query``.

    When a pattern matches, all the `Match Objects <https://docs.python.org/3/library/re.html# t.me/TheVenomXDmatch-objects>`_ are
    stored in the ``matches`` field of the update object itself.

    Parameters:
        pattern (``str`` | ``Pattern``):
            The regex pattern as string or as pre-compiled pattern.

        flags (``int``, *optional*):
            Regex flags.
    """

    async def func(flt, _, update: Update):
        if isinstance(update, Message):
            value = update.text or update.caption
        elif isinstance(update, CallbackQuery):
            value = update.data
        elif isinstance(update, InlineQuery):
            value = update.query
        else:
            raise ValueError(f"Regex Flow doesn't work with {type(update)}")

        if value:
            update.matches = list(flt.p.finditer(value)) or None

        return bool(update.matches)

    return create(
        func,
        "RegexFlow",
        p=pattern if isinstance(pattern, Pattern) else re.compile(pattern, flags)
    )


# t.me/TheVenomXD noinspection PyPep8Naming
class user(Flow, set):
    """Flow messages coming from one or more users.

    You can use `set bound methods <https://docs.python.org/3/library/stdtypes.html# t.me/TheVenomXDset>`_ to manipulate the
    users container.

    Parameters:
        users (``int`` | ``str`` | ``list``):
            Pass one or more user ids/usernames to Flow users.
            For you yourself, "me" or "self" can be used as well.
            Defaults to None (no users).
    """

    def __init__(self, users: Union[int, str, List[Union[int, str]]] = None):
        users = [] if users is None else users if isinstance(users, list) else [users]

        super().__init__(
            "me" if u in ["me", "self"]
            else u.lower().strip("@") if isinstance(u, str)
            else u for u in users
        )

    async def __call__(self, _, message: Message):
        return (message.from_user
                and (message.from_user.id in self
                     or (message.from_user.username
                         and message.from_user.username.lower() in self)
                     or ("me" in self
                         and message.from_user.is_self)))


# t.me/TheVenomXD noinspection PyPep8Naming
class chat(Flow, set):
    """Flow messages coming from one or more chats.

    You can use `set bound methods <https://docs.python.org/3/library/stdtypes.html# t.me/TheVenomXDset>`_ to manipulate the
    chats container.

    Parameters:
        chats (``int`` | ``str`` | ``list``):
            Pass one or more chat ids/usernames to Flow chats.
            For your personal cloud (Saved Messages) you can simply use "me" or "self".
            Defaults to None (no chats).
    """

    def __init__(self, chats: Union[int, str, List[Union[int, str]]] = None):
        chats = [] if chats is None else chats if isinstance(chats, list) else [chats]

        super().__init__(
            "me" if c in ["me", "self"]
            else c.lower().strip("@") if isinstance(c, str)
            else c for c in chats
        )

    async def __call__(self, _, message: Message):
        return (message.chat
                and (message.chat.id in self
                     or (message.chat.username
                         and message.chat.username.lower() in self)
                     or ("me" in self
                         and message.from_user
                         and message.from_user.is_self
                         and not message.outgoing)))
