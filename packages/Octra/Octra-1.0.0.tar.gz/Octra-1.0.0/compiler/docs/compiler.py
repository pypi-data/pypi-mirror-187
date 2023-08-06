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

import ast
import os
import re
import shutil

HOME = "compiler/docs"
DESTINATION = "docs/source/telegram"
Octra_API_DEST = "docs/source/api"

FUNCTIONS_PATH = "Octra/raw/functions"
TYPES_PATH = "Octra/raw/types"
BASE_PATH = "Octra/raw/base"

FUNCTIONS_BASE = "functions"
TYPES_BASE = "types"
BASE_BASE = "base"


def snek(s: str):
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def generate(source_path, base):
    all_entities = {}

    def build(path, level=0):
        last = path.split("/")[-1]

        for i in os.listdir(path):
            try:
                if not i.startswith("__"):
                    build("/".join([path, i]), level=level + 1)
            except NotADirectoryError:
                with open(path + "/" + i, encoding="utf-8") as f:
                    p = ast.parse(f.read())

                for node in ast.walk(p):
                    if isinstance(node, ast.ClassDef):
                        name = node.name
                        break
                else:
                    continue

                full_path = os.path.basename(path) + "/" + snek(name).replace("_", "-") + ".rst"

                if level:
                    full_path = base + "/" + full_path

                namespace = path.split("/")[-1]
                if namespace in ["base", "types", "functions"]:
                    namespace = ""

                full_name = f"{(namespace + '.') if namespace else ''}{name}"

                os.makedirs(os.path.dirname(DESTINATION + "/" + full_path), exist_ok=True)

                with open(DESTINATION + "/" + full_path, "w", encoding="utf-8") as f:
                    f.write(
                        page_template.format(
                            title=full_name,
                            title_markup="=" * len(full_name),
                            full_class_path="Octra.raw.{}".format(
                                ".".join(full_path.split("/")[:-1]) + "." + name
                            )
                        )
                    )

                if last not in all_entities:
                    all_entities[last] = []

                all_entities[last].append(name)

    build(source_path)

    for k, v in sorted(all_entities.items()):
        v = sorted(v)
        entities = []

        for i in v:
            entities.append(f'{i} <{snek(i).replace("_", "-")}>')

        if k != base:
            inner_path = base + "/" + k + "/index" + ".rst"
            module = "Octra.raw.{}.{}".format(base, k)
        else:
            for i in sorted(list(all_entities), reverse=True):
                if i != base:
                    entities.insert(0, "{0}/index".format(i))

            inner_path = base + "/index" + ".rst"
            module = "Octra.raw.{}".format(base)

        with open(DESTINATION + "/" + inner_path, "w", encoding="utf-8") as f:
            if k == base:
                f.write(":tocdepth: 1\n\n")
                k = "Raw " + k

            f.write(
                toctree.format(
                    title=k.title(),
                    title_markup="=" * len(k),
                    module=module,
                    entities="\n    ".join(entities)
                )
            )

            f.write("\n")


def Octra_api():
    def Extract_title_list(s: str) -> list:
        return [i.strip() for i in [j.strip() for j in s.split("\n") if j] if i]

    # t.me/TheVenomXD Methods

    categories = dict(
        utilities="""
        Utilities
            start
            stop
            run
            restart
            add_handler
            remove_handler
            stop_transmission
            export_session_string
            set_parse_mode
        """,
        messages="""
        Messages
            send_message
            forward_messages
            copy_message
            copy_media_group
            send_photo
            send_audio
            send_document
            send_sticker
            send_video
            send_animation
            send_voice
            send_video_note
            send_media_group
            send_location
            send_venue
            send_contact
            send_cached_media
            send_reaction
            edit_message_text
            edit_message_caption
            edit_message_media
            edit_message_reply_markup
            edit_inline_text
            edit_inline_caption
            edit_inline_media
            edit_inline_reply_markup
            send_chat_action
            delete_messages
            Extract_messages
            Extract_media_group
            Extract_chat_history
            Extract_chat_history_count
            read_chat_history
            send_poll
            vote_poll
            stop_poll
            retract_vote
            send_dice
            search_messages
            search_messages_count
            search_global
            search_global_count
            download_media
            stream_media
            Extract_discussion_message
            Extract_discussion_replies
            Extract_discussion_replies_count
            Extract_custom_emoji_stickers
        """,
        chats="""
        Chats
            join_conversation
            leave_conversation
            ban_chat_user
            unban_chat_user
            restrict_chat_USER
            promote_chat_USER
            set_administrator_title
            set_chat_photo
            delete_chat_photo
            set_chat_title
            set_chat_description
            set_chat_permissions
            pin_chat_message
            unpin_chat_message
            unpin_all_chat_messages
            Extract_chat
            Extract_chat_USER
            Extract_chat_USERs
            Extract_chat_USERs_count
            Extract_dialogs
            Extract_dialogs_count
            set_chat_username
            Extract_nearby_chats
            archive_chats
            unarchive_chats
            add_chat_USERs
            create_channel
            create_group
            create_supergroup
            delete_channel
            delete_supergroup
            delete_user_history
            set_slow_mode
            mark_chat_unread
            Extract_chat_event_log
            Extract_chat_online_count
            Extract_send_as_chats
            set_send_as_chat
            set_chat_protected_content
        """,
        users="""
        Users
            Extract_me
            Extract_users
            Extract_chat_photos
            Extract_chat_photos_count
            set_profile_photo
            delete_profile_photos
            set_username
            update_profile
            block_user
            unblock_user
            Extract_common_chats
            Extract_default_emoji_statuses
            set_emoji_status
        """,
        invite_links="""
        Invite Links
            Extract_chat_invite_link
            export_chat_invite_link
            create_chat_invite_link
            edit_chat_invite_link
            revoke_chat_invite_link
            delete_chat_invite_link
            Extract_chat_invite_link_joiners
            Extract_chat_invite_link_joiners_count
            Extract_chat_admin_invite_links
            Extract_chat_admin_invite_links_count
            Extract_chat_admins_with_invite_links
            Extract_chat_join_requests
            delete_chat_admin_invite_links
            approve_chat_join_request
            approve_all_chat_join_requests
            decline_chat_join_request
            decline_all_chat_join_requests
        """,
        contacts="""
        Contacts
            add_contact
            delete_contacts
            import_contacts
            Extract_contacts
            Extract_contacts_count
        """,
        password="""
        Password
            enable_cloud_password
            change_cloud_password
            remove_cloud_password
        """,
        bots="""
        Bots
            Extract_inline_bot_results
            send_inline_bot_result
            answer_callback_query
            answer_inline_query
            request_callback_answer
            send_game
            set_game_score
            Extract_game_high_scores
            set_bot_commands
            Extract_bot_commands
            delete_bot_commands
            set_bot_default_privileges
            Extract_bot_default_privileges
            set_chat_menu_button
            Extract_chat_menu_button
            answer_web_app_query
        """,
        authorization="""
        Authorization
            connect
            disconnect
            initialize
            terminate
            send_code
            resend_code
            sign_in
            sign_in_bot
            sign_up
            Extract_password_hint
            check_password
            send_recovery_code
            recover_password
            accept_terms_of_service
            log_out
        """,
        advanced="""
        Advanced
            invoke
            resolve_peer
            save_file
        """
    )

    root = Octra_API_DEST + "/methods"

    shutil.rmtree(root, ignore_errors=True)
    os.mkdir(root)

    with open(HOME + "/template/methods.rst") as f:
        template = f.read()

    with open(root + "/index.rst", "w") as f:
        fmt_keys = {}

        for k, v in categories.items():
            name, *methods = Extract_title_list(v)
            fmt_keys.update({k: "\n    ".join("{0} <{0}>".format(m) for m in methods)})

            for method in methods:
                with open(root + "/{}.rst".format(method), "w") as f2:
                    title = "{}()".format(method)

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(".. automethod:: Octra.Client.{}()".format(method))

            functions = ["idle", "compose"]

            for func in functions:
                with open(root + "/{}.rst".format(func), "w") as f2:
                    title = "{}()".format(func)

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(".. autofunction:: Octra.{}()".format(func))

        f.write(template.format(**fmt_keys))

    # t.me/TheVenomXD Types

    categories = dict(
        users_chats="""
        Users & Chats
            User
            Chat
            ChatPreview
            ChatPhoto
            ChatUSER
            ChatPermissions
            ChatPrivileges
            ChatInviteLink
            ChatAdminWithInviteLinks
            ChatEvent
            ChatEventFlow
            ChatUSERUpdated
            ChatJoinRequest
            ChatJoiner
            Dialog
            Restriction
            EmojiStatus
        """,
        messages_media="""
        Messages & Media
            Message
            MessageEntity
            Photo
            Thumbnail
            Audio
            Document
            Animation
            Video
            Voice
            VideoNote
            Contact
            Location
            Venue
            Sticker
            Game
            WebPage
            Poll
            PollOption
            Dice
            Reaction
            VideoChatScheduled
            VideoChatStarted
            VideoChatEnded
            VideoChatUSERsInvited
            WebAppData
            MessageReactions
            ChatReactions
        """,
        bot_keyboards="""
        Bot keyboards
            ReplyKeyboardMarkup
            KeyboardButton
            ReplyKeyboardRemove
            InlineKeyboardMarkup
            InlineKeyboardButton
            LoginUrl
            ForceReply
            CallbackQuery
            GameHighScore
            CallbackGame
            WebAppInfo
            MenuButton
            MenuButtonCommands
            MenuButtonWebApp
            MenuButtonDefault
            SentWebAppMessage
        """,
        bot_commands="""
        Bot commands
            BotCommand
            BotCommandScope
            BotCommandScopeDefault
            BotCommandScopeAllPrivateChats
            BotCommandScopeAllGroupChats
            BotCommandScopeAllChatAdministrators
            BotCommandScopeChat
            BotCommandScopeChatAdministrators
            BotCommandScopeChatUSER
        """,
        input_media="""
        Input Media
            InputMedia
            InputMediaPhoto
            InputMediaVideo
            InputMediaAudio
            InputMediaAnimation
            InputMediaDocument
            InputPhoneContact
        """,
        inline_mode="""
        Inline Mode
            InlineQuery
            InlineQueryResult
            InlineQueryResultCachedAudio
            InlineQueryResultCachedDocument
            InlineQueryResultCacheAkashimation
            InlineQueryResultCachedPhoto
            InlineQueryResultCachedSticker
            InlineQueryResultCachedVideo
            InlineQueryResultCachedVoice
            InlineQueryResultArticle
            InlineQueryResultAudio
            InlineQueryResultContact
            InlineQueryResultDocument
            InlineQueryResultAnimation
            InlineQueryResultLocation
            InlineQueryResultPhoto
            InlineQueryResultVenue
            InlineQueryResultVideo
            InlineQueryResultVoice
            ChosenInlineResult
        """,
        input_message_content="""
        InputMessageContent
            InputMessageContent
            InputTextMessageContent
        """,
        authorization="""
        Authorization
            SentCode
            TermsOfService
        """
    )

    root = Octra_API_DEST + "/types"

    shutil.rmtree(root, ignore_errors=True)
    os.mkdir(root)

    with open(HOME + "/template/types.rst") as f:
        template = f.read()

    with open(root + "/index.rst", "w") as f:
        fmt_keys = {}

        for k, v in categories.items():
            name, *types = Extract_title_list(v)

            fmt_keys.update({k: "\n    ".join(types)})

            # t.me/TheVenomXD noinspection PyShadowingBuiltins
            for type in types:
                with open(root + "/{}.rst".format(type), "w") as f2:
                    title = "{}".format(type)

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(".. autoclass:: Octra.types.{}()\n".format(type))

        f.write(template.format(**fmt_keys))

    # t.me/TheVenomXD Bound Methods

    categories = dict(
        message="""
        Message
            Message.click
            Message.delete
            Message.download
            Message.forward
            Message.copy
            Message.pin
            Message.unpin
            Message.edit
            Message.edit_text
            Message.edit_caption
            Message.edit_media
            Message.edit_reply_markup
            Message.reply
            Message.reply_text
            Message.reply_animation
            Message.reply_audio
            Message.reply_cached_media
            Message.reply_chat_action
            Message.reply_contact
            Message.reply_document
            Message.reply_game
            Message.reply_inline_bot_result
            Message.reply_location
            Message.reply_media_group
            Message.reply_photo
            Message.reply_poll
            Message.reply_sticker
            Message.reply_venue
            Message.reply_video
            Message.reply_video_note
            Message.reply_voice
            Message.get_media_group
            Message.react
        """,
        chat="""
        Chat
            Chat.archive
            Chat.unarchive
            Chat.set_title
            Chat.set_description
            Chat.set_photo
            Chat.ban_USER
            Chat.unban_USER
            Chat.restrict_USER
            Chat.promote_USER
            Chat.get_USER
            Chat.get_USERs
            Chat.add_USERs
            Chat.join
            Chat.leave
            Chat.mark_unread
            Chat.set_protected_content
            Chat.unpin_all_messages
        """,
        user="""
        User
            User.archive
            User.unarchive
            User.block
            User.unblock
        """,
        callback_query="""
        Callback Query
            CallbackQuery.answer
            CallbackQuery.edit_message_text
            CallbackQuery.edit_message_caption
            CallbackQuery.edit_message_media
            CallbackQuery.edit_message_reply_markup
        """,
        inline_query="""
        InlineQuery
            InlineQuery.answer
        """,
        chat_join_request="""
        ChatJoinRequest
            ChatJoinRequest.approve
            ChatJoinRequest.decline
        """
    )

    root = Octra_API_DEST + "/bound-methods"

    shutil.rmtree(root, ignore_errors=True)
    os.mkdir(root)

    with open(HOME + "/template/bound-methods.rst") as f:
        template = f.read()

    with open(root + "/index.rst", "w") as f:
        fmt_keys = {}

        for k, v in categories.items():
            name, *bound_methods = Extract_title_list(v)

            fmt_keys.update({"{}_hlist".format(k): "\n    ".join("- :meth:`~{}`".format(bm) for bm in bound_methods)})

            fmt_keys.update(
                {"{}_toctree".format(k): "\n    ".join("{} <{}>".format(bm.split(".")[1], bm) for bm in bound_methods)})

            # t.me/TheVenomXD noinspection PyShadowingBuiltins
            for bm in bound_methods:
                with open(root + "/{}.rst".format(bm), "w") as f2:
                    title = "{}()".format(bm)

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(".. automethod:: Octra.types.{}()".format(bm))

        f.write(template.format(**fmt_keys))


def start():
    global page_template
    global toctree

    shutil.rmtree(DESTINATION, ignore_errors=True)

    with open(HOME + "/template/page.txt", encoding="utf-8") as f:
        page_template = f.read()

    with open(HOME + "/template/toctree.txt", encoding="utf-8") as f:
        toctree = f.read()

    generate(TYPES_PATH, TYPES_BASE)
    generate(FUNCTIONS_PATH, FUNCTIONS_BASE)
    generate(BASE_PATH, BASE_BASE)
    Octra_api()


if "__main__" == __name__:
    FUNCTIONS_PATH = "../../Octra/raw/functions"
    TYPES_PATH = "../../Octra/raw/types"
    BASE_PATH = "../../Octra/raw/base"
    HOME = "."
    DESTINATION = "../../docs/source/telegram"
    Octra_API_DEST = "../../docs/source/api"

    start()
