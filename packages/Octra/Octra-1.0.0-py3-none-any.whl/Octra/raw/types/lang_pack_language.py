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

from io import BytesIO

from Octra.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from Octra.raw.core import TLObject
from Octra import raw
from typing import List, Optional, Any

# t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD
# t.me/TheVenomXD               !!! WARNING !!!               # t.me/TheVenomXD
# t.me/TheVenomXD          This is a generated file!          # t.me/TheVenomXD
# t.me/TheVenomXD All changes made in this file will be lost! # t.me/TheVenomXD
# t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD # t.me/TheVenomXD


class LangPackLanguage(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.LangPackLanguage`.

    Details:
        - Layer: ``151``
        - ID: ``EECA5CE3``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD official <Octra.raw.base.# t.me/TheVenomXD official>`):
            N/A

        name (:obj:`string native_name <Octra.raw.base.string native_name>`):
            N/A

        lang_code (:obj:`string base_lang_code <Octra.raw.base.string base_lang_code>`):
            N/A

        plural_code (:obj:`string strings_count <Octra.raw.base.string strings_count>`):
            N/A

        translated_count (:obj:`int translations_url <Octra.raw.base.int translations_url>`):
            N/A

        rtl (:obj:`true beta <Octra.raw.base.true beta>`, *optional*):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            langpack.GetLanguages
            langpack.GetLanguage
    """

    __slots__: List[str] = ["flags", "name", "lang_code", "plural_code", "translated_count", "rtl"]

    ID = 0xeeca5ce3
    QUALNAME = "types.LangPackLanguage"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD official", name: "raw.base.string native_name", lang_code: "raw.base.string base_lang_code", plural_code: "raw.base.string strings_count", translated_count: "raw.base.int translations_url", rtl: "raw.base.true beta" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD official
        self.name = name  # t.me/TheVenomXD string native_name
        self.lang_code = lang_code  # t.me/TheVenomXD string base_lang_code
        self.plural_code = plural_code  # t.me/TheVenomXD string strings_count
        self.translated_count = translated_count  # t.me/TheVenomXD int translations_url
        self.rtl = rtl  # t.me/TheVenomXD flags.2?true beta

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "LangPackLanguage":
        
        flags = TLObject.read(b)
        
        rtl = True if flags & (1 << 2) else False
        name = TLObject.read(b)
        
        lang_code = TLObject.read(b)
        
        plural_code = TLObject.read(b)
        
        translated_count = TLObject.read(b)
        
        return LangPackLanguage(flags=flags, name=name, lang_code=lang_code, plural_code=plural_code, translated_count=translated_count, rtl=rtl)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.name.write())
        
        b.write(self.lang_code.write())
        
        b.write(self.plural_code.write())
        
        b.write(self.translated_count.write())
        
        return b.getvalue()
