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

from typing import List, Union, BinaryIO

from ..messages_and_media import MessageEntity
from ..object import Object


class InputMedia(Object):
    """Content of a media message to be sent.

    It should be one of:

    - :obj:`~Octra.types.InputMediaAnimation`
    - :obj:`~Octra.types.InputMediaDocument`
    - :obj:`~Octra.types.InputMediaAudio`
    - :obj:`~Octra.types.InputMediaPhoto`
    - :obj:`~Octra.types.InputMediaVideo`
    """

    def __init__(
        self,
        media: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: str = None,
        caption_entities: List[MessageEntity] = None
    ):
        super().__init__()

        self.media = media
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
