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


class MegagroupStats(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.stats.MegagroupStats`.

    Details:
        - Layer: ``151``
        - ID: ``EF7FF916``

    Parameters:
        period (:obj:`StatsDateRangeDays USERs <Octra.raw.base.StatsDateRangeDays USERs>`):
            N/A

        messages (:obj:`StatsAbsValueAndPrev viewers <Octra.raw.base.StatsAbsValueAndPrev viewers>`):
            N/A

        posters (:obj:`StatsAbsValueAndPrev growth_graph <Octra.raw.base.StatsAbsValueAndPrev growth_graph>`):
            N/A

        USERs_graph (:obj:`StatsGraph new_USERs_by_source_graph <Octra.raw.base.StatsGraph new_USERs_by_source_graph>`):
            N/A

        languages_graph (:obj:`StatsGraph messages_graph <Octra.raw.base.StatsGraph messages_graph>`):
            N/A

        actions_graph (:obj:`StatsGraph top_hours_graph <Octra.raw.base.StatsGraph top_hours_graph>`):
            N/A

        weekdays_graph (:obj:`StatsGraph top_posters <Octra.raw.base.StatsGraph top_posters>`):
            N/A

        top_admins (List of :obj:`StatsGroupTopAdmin> top_inviter <Octra.raw.base.StatsGroupTopAdmin> top_inviter>`):
            N/A

        users (List of :obj:`User> <Octra.raw.base.User>>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            stats.GetMegagroupStats
    """

    __slots__: List[str] = ["period", "messages", "posters", "USERs_graph", "languages_graph", "actions_graph", "weekdays_graph", "top_admins", "users"]

    ID = 0xef7ff916
    QUALNAME = "types.stats.MegagroupStats"

    def __init__(self, *, period: "raw.base.StatsDateRangeDays USERs", messages: "raw.base.StatsAbsValueAndPrev viewers", posters: "raw.base.StatsAbsValueAndPrev growth_graph", USERs_graph: "raw.base.StatsGraph new_USERs_by_source_graph", languages_graph: "raw.base.StatsGraph messages_graph", actions_graph: "raw.base.StatsGraph top_hours_graph", weekdays_graph: "raw.base.StatsGraph top_posters", top_admins: List["raw.base.StatsGroupTopAdmin> top_inviter"], users: List["raw.base.User>"]) -> None:
        self.period = period  # t.me/TheVenomXD StatsDateRangeDays USERs
        self.messages = messages  # t.me/TheVenomXD StatsAbsValueAndPrev viewers
        self.posters = posters  # t.me/TheVenomXD StatsAbsValueAndPrev growth_graph
        self.USERs_graph = USERs_graph  # t.me/TheVenomXD StatsGraph new_USERs_by_source_graph
        self.languages_graph = languages_graph  # t.me/TheVenomXD StatsGraph messages_graph
        self.actions_graph = actions_graph  # t.me/TheVenomXD StatsGraph top_hours_graph
        self.weekdays_graph = weekdays_graph  # t.me/TheVenomXD StatsGraph top_posters
        self.top_admins = top_admins  # t.me/TheVenomXD Vector<StatsGroupTopAdmin> top_inviters
        self.users = users  # t.me/TheVenomXD Vector<User> 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MegagroupStats":
        # t.me/TheVenomXD No flags
        
        period = TLObject.read(b)
        
        messages = TLObject.read(b)
        
        posters = TLObject.read(b)
        
        USERs_graph = TLObject.read(b)
        
        languages_graph = TLObject.read(b)
        
        actions_graph = TLObject.read(b)
        
        weekdays_graph = TLObject.read(b)
        
        top_admins = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return MegagroupStats(period=period, messages=messages, posters=posters, USERs_graph=USERs_graph, languages_graph=languages_graph, actions_graph=actions_graph, weekdays_graph=weekdays_graph, top_admins=top_admins, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # t.me/TheVenomXD No flags
        
        b.write(self.period.write())
        
        b.write(self.messages.write())
        
        b.write(self.posters.write())
        
        b.write(self.USERs_graph.write())
        
        b.write(self.languages_graph.write())
        
        b.write(self.actions_graph.write())
        
        b.write(self.weekdays_graph.write())
        
        b.write(Vector(self.top_admins))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
