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


class DialogFlow(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.DialogFlow`.

    Details:
        - Layer: ``151``
        - ID: ``7438F7E8``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD contacts <Octra.raw.base.# t.me/TheVenomXD contacts>`):
            N/A

        title (:obj:`string emoticon <Octra.raw.base.string emoticon>`):
            N/A

        pinned_peers (List of :obj:`InputPeer> include_peer <Octra.raw.base.InputPeer> include_peer>`):
            N/A

        exclude_peers (List of :obj:`InputPeer> <Octra.raw.base.InputPeer>>`):
            N/A

        non_contacts (:obj:`true groups <Octra.raw.base.true groups>`, *optional*):
            N/A

        broadcasts (:obj:`true bots <Octra.raw.base.true bots>`, *optional*):
            N/A

        exclude_muted (:obj:`true exclude_read <Octra.raw.base.true exclude_read>`, *optional*):
            N/A

        exclude_archived (:obj:`true id <Octra.raw.base.true id>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetDialogFlows
    """

    __slots__: List[str] = ["flags", "title", "pinned_peers", "exclude_peers", "non_contacts", "broadcasts", "exclude_muted", "exclude_archived"]

    ID = 0x7438f7e8
    QUALNAME = "types.DialogFlow"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD contacts", title: "raw.base.string emoticon", pinned_peers: List["raw.base.InputPeer> include_peer"], exclude_peers: List["raw.base.InputPeer>"], non_contacts: "raw.base.true groups" = None, broadcasts: "raw.base.true bots" = None, exclude_muted: "raw.base.true exclude_read" = None, exclude_archived: "raw.base.true id" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD contacts
        self.title = title  # t.me/TheVenomXD string emoticon
        self.pinned_peers = pinned_peers  # t.me/TheVenomXD Vector<InputPeer> include_peers
        self.exclude_peers = exclude_peers  # t.me/TheVenomXD Vector<InputPeer> 
        self.non_contacts = non_contacts  # t.me/TheVenomXD flags.1?true groups
        self.broadcasts = broadcasts  # t.me/TheVenomXD flags.3?true bots
        self.exclude_muted = exclude_muted  # t.me/TheVenomXD flags.11?true exclude_read
        self.exclude_archived = exclude_archived  # t.me/TheVenomXD flags.13?true id

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DialogFlow":
        
        flags = TLObject.read(b)
        
        non_contacts = True if flags & (1 << 1) else False
        broadcasts = True if flags & (1 << 3) else False
        exclude_muted = True if flags & (1 << 11) else False
        exclude_archived = True if flags & (1 << 13) else False
        title = TLObject.read(b)
        
        pinned_peers = TLObject.read(b)
        
        exclude_peers = TLObject.read(b)
        
        return DialogFlow(flags=flags, title=title, pinned_peers=pinned_peers, exclude_peers=exclude_peers, non_contacts=non_contacts, broadcasts=broadcasts, exclude_muted=exclude_muted, exclude_archived=exclude_archived)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.title.write())
        
        b.write(Vector(self.pinned_peers))
        
        b.write(Vector(self.exclude_peers))
        
        return b.getvalue()
