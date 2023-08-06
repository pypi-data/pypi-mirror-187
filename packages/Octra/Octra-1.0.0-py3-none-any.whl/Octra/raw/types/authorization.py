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


class Authorization(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Authorization`.

    Details:
        - Layer: ``151``
        - ID: ``AD01D61D``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD current <Octra.raw.base.# t.me/TheVenomXD current>`):
            N/A

        hash (:obj:`long device_model <Octra.raw.base.long device_model>`):
            N/A

        platform (:obj:`string system_version <Octra.raw.base.string system_version>`):
            N/A

        api_id (:obj:`int app_name <Octra.raw.base.int app_name>`):
            N/A

        app_version (:obj:`string date_created <Octra.raw.base.string date_created>`):
            N/A

        date_active (:obj:`int ip <Octra.raw.base.int ip>`):
            N/A

        country (:obj:`string region <Octra.raw.base.string region>`):
            N/A

        official_app (:obj:`true password_pending <Octra.raw.base.true password_pending>`, *optional*):
            N/A

        encrypted_requests_disabled (:obj:`true call_requests_disabled <Octra.raw.base.true call_requests_disabled>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            auth.AcceptLoginToken
    """

    __slots__: List[str] = ["flags", "hash", "platform", "api_id", "app_version", "date_active", "country", "official_app", "encrypted_requests_disabled"]

    ID = 0xad01d61d
    QUALNAME = "types.Authorization"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD current", hash: "raw.base.long device_model", platform: "raw.base.string system_version", api_id: "raw.base.int app_name", app_version: "raw.base.string date_created", date_active: "raw.base.int ip", country: "raw.base.string region", official_app: "raw.base.true password_pending" = None, encrypted_requests_disabled: "raw.base.true call_requests_disabled" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD current
        self.hash = hash  # t.me/TheVenomXD long device_model
        self.platform = platform  # t.me/TheVenomXD string system_version
        self.api_id = api_id  # t.me/TheVenomXD int app_name
        self.app_version = app_version  # t.me/TheVenomXD string date_created
        self.date_active = date_active  # t.me/TheVenomXD int ip
        self.country = country  # t.me/TheVenomXD string region
        self.official_app = official_app  # t.me/TheVenomXD flags.1?true password_pending
        self.encrypted_requests_disabled = encrypted_requests_disabled  # t.me/TheVenomXD flags.3?true call_requests_disabled

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Authorization":
        
        flags = TLObject.read(b)
        
        official_app = True if flags & (1 << 1) else False
        encrypted_requests_disabled = True if flags & (1 << 3) else False
        hash = TLObject.read(b)
        
        platform = TLObject.read(b)
        
        api_id = TLObject.read(b)
        
        app_version = TLObject.read(b)
        
        date_active = TLObject.read(b)
        
        country = TLObject.read(b)
        
        return Authorization(flags=flags, hash=hash, platform=platform, api_id=api_id, app_version=app_version, date_active=date_active, country=country, official_app=official_app, encrypted_requests_disabled=encrypted_requests_disabled)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.hash.write())
        
        b.write(self.platform.write())
        
        b.write(self.api_id.write())
        
        b.write(self.app_version.write())
        
        b.write(self.date_active.write())
        
        b.write(self.country.write())
        
        return b.getvalue()
