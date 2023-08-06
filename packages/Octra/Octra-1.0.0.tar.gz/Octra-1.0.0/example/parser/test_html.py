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
from Octra.parser.html import HTML


# t.me/TheVenomXD expected: the expected unparsed HTML
# t.me/TheVenomXD text: original text without entities
# t.me/TheVenomXD entities: message entities coming from the server

def test_html_unparse_bold():
    expected = "<b>bold</b>"
    text = "bold"
    entities = Octra.types.List(
        [Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.BOLD, offset=0, length=4)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_italic():
    expected = "<i>italic</i>"
    text = "italic"
    entities = Octra.types.List(
        [Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.ITALIC, offset=0, length=6)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_underline():
    expected = "<u>underline</u>"
    text = "underline"
    entities = Octra.types.List(
        [Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.UNDERLINE, offset=0, length=9)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_strike():
    expected = "<s>strike</s>"
    text = "strike"
    entities = Octra.types.List(
        [Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.STRIKETHROUGH, offset=0, length=6)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_spoiler():
    expected = "<spoiler>spoiler</spoiler>"
    text = "spoiler"
    entities = Octra.types.List(
        [Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.SPOILER, offset=0, length=7)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_url():
    expected = '<a href="https://Octra.org/">URL</a>'
    text = "URL"
    entities = Octra.types.List([Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.TEXT_LINK,
                                                                 offset=0, length=3, url='https://Octra.org/')])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_code():
    expected = '<code>code</code>'
    text = "code"
    entities = Octra.types.List(
        [Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.CODE, offset=0, length=4)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_pre():
    expected = """<pre language="python">for i in range(10):
    print(i)</pre>"""

    text = """for i in range(10):
    print(i)"""

    entities = Octra.types.List([Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.PRE, offset=0,
                                                                 length=32, language='python')])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_mixed():
    expected = "<b>aaaaaaa<i>aaa<u>bbbb</u></i></b><u><i>bbbbbbccc</i></u><u>ccccccc<s>ddd</s></u><s>ddddd<spoiler>dd" \
               "eee</spoiler></s><spoiler>eeeeeeefff</spoiler>ffff<code>fffggggggg</code>ggghhhhhhhhhh"
    text = "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhh"
    entities = Octra.types.List(
        [Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.BOLD, offset=0, length=14),
         Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.ITALIC, offset=7, length=7),
         Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.UNDERLINE, offset=10, length=4),
         Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.UNDERLINE, offset=14, length=9),
         Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.ITALIC, offset=14, length=9),
         Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.UNDERLINE, offset=23, length=10),
         Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.STRIKETHROUGH, offset=30, length=3),
         Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.STRIKETHROUGH, offset=33, length=10),
         Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.SPOILER, offset=38, length=5),
         Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.SPOILER, offset=43, length=10),
         Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.CODE, offset=57, length=10)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_escaped():
    expected = "<b>&lt;b&gt;bold&lt;/b&gt;</b>"
    text = "<b>bold</b>"
    entities = Octra.types.List(
        [Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.BOLD, offset=0, length=11)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_escaped_nested():
    expected = "<b>&lt;b&gt;bold <u>&lt;u&gt;underline&lt;/u&gt;</u> bold&lt;/b&gt;</b>"
    text = "<b>bold <u>underline</u> bold</b>"
    entities = Octra.types.List(
        [Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.BOLD, offset=0, length=33),
         Octra.types.MessageEntity(type=Octra.enums.MessageEntityType.UNDERLINE, offset=8, length=16)])

    assert HTML.unparse(text=text, entities=entities) == expected


def test_html_unparse_no_entities():
    expected = "text"
    text = "text"
    entities = []

    assert HTML.unparse(text=text, entities=entities) == expected
