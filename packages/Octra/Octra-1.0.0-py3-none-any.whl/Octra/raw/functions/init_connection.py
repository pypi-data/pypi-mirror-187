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


class InitConnection(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API function.

    Details:
        - Layer: ``151``
        - ID: ``C1CD5EA9``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD api_id <Octra.raw.base.# t.me/TheVenomXD api_id>`):
            N/A

        device_model (:obj:`string system_version <Octra.raw.base.string system_version>`):
            N/A

        app_version (:obj:`string system_lang_code <Octra.raw.base.string system_lang_code>`):
            N/A

        lang_pack (:obj:`string lang_code <Octra.raw.base.string lang_code>`):
            N/A

        query (:obj:`!X  <Octra.raw.base.!X >`):
            N/A

        proxy (:obj:`InputClientProxy params <Octra.raw.base.InputClientProxy params>`, *optional*):
            N/A

    Returns:
        Any object from :obj:`~Octra.raw.types`
    """

    __slots__: List[str] = ["flags", "device_model", "app_version", "lang_pack", "query", "proxy"]

    ID = 0xc1cd5ea9
    QUALNAME = "functions.InitConnection"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD api_id", device_model: "raw.base.string system_version", app_version: "raw.base.string system_lang_code", lang_pack: "raw.base.string lang_code", query: "raw.base.!X ", proxy: "raw.base.InputClientProxy params" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD api_id
        self.device_model = device_model  # t.me/TheVenomXD string system_version
        self.app_version = app_version  # t.me/TheVenomXD string system_lang_code
        self.lang_pack = lang_pack  # t.me/TheVenomXD string lang_code
        self.query = query  # t.me/TheVenomXD !X 
        self.proxy = proxy  # t.me/TheVenomXD flags.0?InputClientProxy params

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InitConnection":
        
        flags = TLObject.read(b)
        
        device_model = TLObject.read(b)
        
        app_version = TLObject.read(b)
        
        lang_pack = TLObject.read(b)
        
        proxy = TLObject.read(b) if flags & (1 << 0) else None
        
        query = TLObject.read(b)
        
        return InitConnection(flags=flags, device_model=device_model, app_version=app_version, lang_pack=lang_pack, query=query, proxy=proxy)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.device_model.write())
        
        b.write(self.app_version.write())
        
        b.write(self.lang_pack.write())
        
        if self.proxy is not None:
            b.write(self.proxy.write())
        
        b.write(self.query.write())
        
        return b.getvalue()
