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


class PremiumPromo(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.help.PremiumPromo`.

    Details:
        - Layer: ``151``
        - ID: ``5334759C``

    Parameters:
        status_text (:obj:`string status_entities <Octra.raw.base.string status_entities>`):
            N/A

        video_sections (List of :obj:`string> video <Octra.raw.base.string> video>`):
            N/A

        period_options (List of :obj:`PremiumSubscriptionOption> user <Octra.raw.base.PremiumSubscriptionOption> user>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            help.GetPremiumPromo
    """

    __slots__: List[str] = ["status_text", "video_sections", "period_options"]

    ID = 0x5334759c
    QUALNAME = "types.help.PremiumPromo"

    def __init__(self, *, status_text: "raw.base.string status_entities", video_sections: List["raw.base.string> video"], period_options: List["raw.base.PremiumSubscriptionOption> user"]) -> None:
        self.status_text = status_text  # t.me/TheVenomXD string status_entities
        self.video_sections = video_sections  # t.me/TheVenomXD Vector<string> videos
        self.period_options = period_options  # t.me/TheVenomXD Vector<PremiumSubscriptionOption> users

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PremiumPromo":
        # t.me/TheVenomXD No flags
        
        status_text = TLObject.read(b)
        
        video_sections = TLObject.read(b)
        
        period_options = TLObject.read(b)
        
        return PremiumPromo(status_text=status_text, video_sections=video_sections, period_options=period_options)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # t.me/TheVenomXD No flags
        
        b.write(self.status_text.write())
        
        b.write(Vector(self.video_sections))
        
        b.write(Vector(self.period_options))
        
        return b.getvalue()
