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


class BroadcastStats(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.stats.BroadcastStats`.

    Details:
        - Layer: ``151``
        - ID: ``BDF78394``

    Parameters:
        period (:obj:`StatsDateRangeDays followers <Octra.raw.base.StatsDateRangeDays followers>`):
            N/A

        views_per_post (:obj:`StatsAbsValueAndPrev shares_per_post <Octra.raw.base.StatsAbsValueAndPrev shares_per_post>`):
            N/A

        enabled_notifications (:obj:`StatsPercentValue growth_graph <Octra.raw.base.StatsPercentValue growth_graph>`):
            N/A

        followers_graph (:obj:`StatsGraph mute_graph <Octra.raw.base.StatsGraph mute_graph>`):
            N/A

        top_hours_graph (:obj:`StatsGraph interactions_graph <Octra.raw.base.StatsGraph interactions_graph>`):
            N/A

        iv_interactions_graph (:obj:`StatsGraph views_by_source_graph <Octra.raw.base.StatsGraph views_by_source_graph>`):
            N/A

        new_followers_by_source_graph (:obj:`StatsGraph languages_graph <Octra.raw.base.StatsGraph languages_graph>`):
            N/A

        recent_message_interactions (List of :obj:`MessageInteractionCounters> <Octra.raw.base.MessageInteractionCounters>>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            stats.GetBroadcastStats
    """

    __slots__: List[str] = ["period", "views_per_post", "enabled_notifications", "followers_graph", "top_hours_graph", "iv_interactions_graph", "new_followers_by_source_graph", "recent_message_interactions"]

    ID = 0xbdf78394
    QUALNAME = "types.stats.BroadcastStats"

    def __init__(self, *, period: "raw.base.StatsDateRangeDays followers", views_per_post: "raw.base.StatsAbsValueAndPrev shares_per_post", enabled_notifications: "raw.base.StatsPercentValue growth_graph", followers_graph: "raw.base.StatsGraph mute_graph", top_hours_graph: "raw.base.StatsGraph interactions_graph", iv_interactions_graph: "raw.base.StatsGraph views_by_source_graph", new_followers_by_source_graph: "raw.base.StatsGraph languages_graph", recent_message_interactions: List["raw.base.MessageInteractionCounters>"]) -> None:
        self.period = period  # t.me/TheVenomXD StatsDateRangeDays followers
        self.views_per_post = views_per_post  # t.me/TheVenomXD StatsAbsValueAndPrev shares_per_post
        self.enabled_notifications = enabled_notifications  # t.me/TheVenomXD StatsPercentValue growth_graph
        self.followers_graph = followers_graph  # t.me/TheVenomXD StatsGraph mute_graph
        self.top_hours_graph = top_hours_graph  # t.me/TheVenomXD StatsGraph interactions_graph
        self.iv_interactions_graph = iv_interactions_graph  # t.me/TheVenomXD StatsGraph views_by_source_graph
        self.new_followers_by_source_graph = new_followers_by_source_graph  # t.me/TheVenomXD StatsGraph languages_graph
        self.recent_message_interactions = recent_message_interactions  # t.me/TheVenomXD Vector<MessageInteractionCounters> 

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BroadcastStats":
        # t.me/TheVenomXD No flags
        
        period = TLObject.read(b)
        
        views_per_post = TLObject.read(b)
        
        enabled_notifications = TLObject.read(b)
        
        followers_graph = TLObject.read(b)
        
        top_hours_graph = TLObject.read(b)
        
        iv_interactions_graph = TLObject.read(b)
        
        new_followers_by_source_graph = TLObject.read(b)
        
        recent_message_interactions = TLObject.read(b)
        
        return BroadcastStats(period=period, views_per_post=views_per_post, enabled_notifications=enabled_notifications, followers_graph=followers_graph, top_hours_graph=top_hours_graph, iv_interactions_graph=iv_interactions_graph, new_followers_by_source_graph=new_followers_by_source_graph, recent_message_interactions=recent_message_interactions)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # t.me/TheVenomXD No flags
        
        b.write(self.period.write())
        
        b.write(self.views_per_post.write())
        
        b.write(self.enabled_notifications.write())
        
        b.write(self.followers_graph.write())
        
        b.write(self.top_hours_graph.write())
        
        b.write(self.iv_interactions_graph.write())
        
        b.write(self.new_followers_by_source_graph.write())
        
        b.write(Vector(self.recent_message_interactions))
        
        return b.getvalue()
