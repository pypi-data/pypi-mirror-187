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
from Octra import raw
from Octra import types
from ..object import Object


class Game(Object):
    """A game.
    Use BotFather to create and edit games, their short names will act as unique identifiers.

    Parameters:
        id (``int``):
            Unique identifier of the game.

        title (``str``):
            Title of the game.

        short_name (``str``):
            Unique short name of the game.

        description (``str``):
            Description of the game.

        photo (:obj:`~Octra.types.Photo`):
            Photo that will be displayed in the game message in chats.

        animation (:obj:`~Octra.types.Animation`, *optional*):
            Animation that will be displayed in the game message in chats.
            Upload via BotFather.
    """

    def __init__(
        self,
        *,
        client: "Octra.Client" = None,
        id: int,
        title: str,
        short_name: str,
        description: str,
        photo: "types.Photo",
        animation: "types.Animation" = None
    ):
        super().__init__(client)

        self.id = id
        self.title = title
        self.short_name = short_name
        self.description = description
        self.photo = photo
        self.animation = animation

    @staticmethod
    def _parse(client, message: "raw.types.Message") -> "Game":
        game: "raw.types.Game" = message.media.game
        animation = None

        if game.document:
            attributes = {type(i): i for i in game.document.attributes}

            file_name = getattr(
                attributes.get(
                    raw.types.DocumentAttributeFilename, None
                ), "file_name", None
            )

            animation = types.Animation._parse(
                client,
                game.document,
                attributes.get(raw.types.DocumentAttributeVideo, None),
                file_name
            )

        return Game(
            id=game.id,
            title=game.title,
            short_name=game.short_name,
            description=game.description,
            photo=types.Photo._parse(client, game.photo),
            animation=animation,
            client=client
        )
