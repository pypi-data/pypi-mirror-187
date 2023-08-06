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


class Config(TLObject):  # t.me/TheVenomXD type: ignore
    """Telegram API type.

    Constructor of :obj:`~Octra.raw.base.Config`.

    Details:
        - Layer: ``151``
        - ID: ``232566AC``

    Parameters:
        flags (:obj:`# t.me/TheVenomXD phonecalls_enabled <Octra.raw.base.# t.me/TheVenomXD phonecalls_enabled>`):
            N/A

        expires (:obj:`int octra_test_mode <Octra.raw.base.int octra_test_mode>`):
            N/A

        this_dc (:obj:`int dc_options <Octra.raw.base.int dc_options>`):
            N/A

        dc_txt_domain_name (:obj:`string chat_size_max <Octra.raw.base.string chat_size_max>`):
            N/A

        megagroup_size_max (:obj:`int forwarded_count_max <Octra.raw.base.int forwarded_count_max>`):
            N/A

        online_update_period_ms (:obj:`int offline_blur_timeout_ms <Octra.raw.base.int offline_blur_timeout_ms>`):
            N/A

        offline_idle_timeout_ms (:obj:`int online_cloud_timeout_ms <Octra.raw.base.int online_cloud_timeout_ms>`):
            N/A

        notify_cloud_delay_ms (:obj:`int notify_default_delay_ms <Octra.raw.base.int notify_default_delay_ms>`):
            N/A

        push_chat_period_ms (:obj:`int push_chat_limit <Octra.raw.base.int push_chat_limit>`):
            N/A

        saved_gifs_limit (:obj:`int edit_time_limit <Octra.raw.base.int edit_time_limit>`):
            N/A

        revoke_time_limit (:obj:`int revoke_pm_time_limit <Octra.raw.base.int revoke_pm_time_limit>`):
            N/A

        rating_e_decay (:obj:`int stickers_recent_limit <Octra.raw.base.int stickers_recent_limit>`):
            N/A

        stickers_faved_limit (:obj:`int channels_read_media_period <Octra.raw.base.int channels_read_media_period>`):
            N/A

        pinned_infolder_count_max (:obj:`int call_receive_timeout_ms <Octra.raw.base.int call_receive_timeout_ms>`):
            N/A

        call_ring_timeout_ms (:obj:`int call_connect_timeout_ms <Octra.raw.base.int call_connect_timeout_ms>`):
            N/A

        call_packet_timeout_ms (:obj:`int me_url_prefix <Octra.raw.base.int me_url_prefix>`):
            N/A

        message_length_max (:obj:`int webfile_octra_dc_id_ <Octra.raw.base.int webfile_octra_dc_id_>`):
            N/A

        default_p2p_contacts (:obj:`true preload_featured_stickers <Octra.raw.base.true preload_featured_stickers>`, *optional*):
            N/A

        ignore_phone_entities (:obj:`true revoke_pm_inbox <Octra.raw.base.true revoke_pm_inbox>`, *optional*):
            N/A

        blocked_mode (:obj:`true pfs_enabled <Octra.raw.base.true pfs_enabled>`, *optional*):
            N/A

        force_try_ipv6 (:obj:`true date <Octra.raw.base.true date>`, *optional*):
            N/A

        tmp_sessions (:obj:`int pinned_dialogs_count_max <Octra.raw.base.int pinned_dialogs_count_max>`, *optional*):
            N/A

        autoupdate_url_prefix (:obj:`string gif_search_username <Octra.raw.base.string gif_search_username>`, *optional*):
            N/A

        venue_search_username (:obj:`string img_search_username <Octra.raw.base.string img_search_username>`, *optional*):
            N/A

        static_maps_provider (:obj:`string caption_length_max <Octra.raw.base.string caption_length_max>`, *optional*):
            N/A

        suggested_lang_code (:obj:`string lang_pack_version <Octra.raw.base.string lang_pack_version>`, *optional*):
            N/A

        base_lang_pack_version (:obj:`int reactions_default <Octra.raw.base.int reactions_default>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Octra.raw.functions

        .. autosummary::
            :nosignatures:

            help.GetConfig
    """

    __slots__: List[str] = ["flags", "expires", "this_dc", "dc_txt_domain_name", "megagroup_size_max", "online_update_period_ms", "offline_idle_timeout_ms", "notify_cloud_delay_ms", "push_chat_period_ms", "saved_gifs_limit", "revoke_time_limit", "rating_e_decay", "stickers_faved_limit", "pinned_infolder_count_max", "call_ring_timeout_ms", "call_packet_timeout_ms", "message_length_max", "default_p2p_contacts", "ignore_phone_entities", "blocked_mode", "force_try_ipv6", "tmp_sessions", "autoupdate_url_prefix", "venue_search_username", "static_maps_provider", "suggested_lang_code", "base_lang_pack_version"]

    ID = 0x232566ac
    QUALNAME = "types.Config"

    def __init__(self, *, flags: "raw.base.# t.me/TheVenomXD phonecalls_enabled", expires: "raw.base.int octra_test_mode", this_dc: "raw.base.int dc_options", dc_txt_domain_name: "raw.base.string chat_size_max", megagroup_size_max: "raw.base.int forwarded_count_max", online_update_period_ms: "raw.base.int offline_blur_timeout_ms", offline_idle_timeout_ms: "raw.base.int online_cloud_timeout_ms", notify_cloud_delay_ms: "raw.base.int notify_default_delay_ms", push_chat_period_ms: "raw.base.int push_chat_limit", saved_gifs_limit: "raw.base.int edit_time_limit", revoke_time_limit: "raw.base.int revoke_pm_time_limit", rating_e_decay: "raw.base.int stickers_recent_limit", stickers_faved_limit: "raw.base.int channels_read_media_period", pinned_infolder_count_max: "raw.base.int call_receive_timeout_ms", call_ring_timeout_ms: "raw.base.int call_connect_timeout_ms", call_packet_timeout_ms: "raw.base.int me_url_prefix", message_length_max: "raw.base.int webfile_octra_dc_id_", default_p2p_contacts: "raw.base.true preload_featured_stickers" = None, ignore_phone_entities: "raw.base.true revoke_pm_inbox" = None, blocked_mode: "raw.base.true pfs_enabled" = None, force_try_ipv6: "raw.base.true date" = None, tmp_sessions: "raw.base.int pinned_dialogs_count_max" = None, autoupdate_url_prefix: "raw.base.string gif_search_username" = None, venue_search_username: "raw.base.string img_search_username" = None, static_maps_provider: "raw.base.string caption_length_max" = None, suggested_lang_code: "raw.base.string lang_pack_version" = None, base_lang_pack_version: "raw.base.int reactions_default" = None) -> None:
        self.flags = flags  # t.me/TheVenomXD # t.me/TheVenomXD phonecalls_enabled
        self.expires = expires  # t.me/TheVenomXD int octra_test_mode
        self.this_dc = this_dc  # t.me/TheVenomXD int dc_options
        self.dc_txt_domain_name = dc_txt_domain_name  # t.me/TheVenomXD string chat_size_max
        self.megagroup_size_max = megagroup_size_max  # t.me/TheVenomXD int forwarded_count_max
        self.online_update_period_ms = online_update_period_ms  # t.me/TheVenomXD int offline_blur_timeout_ms
        self.offline_idle_timeout_ms = offline_idle_timeout_ms  # t.me/TheVenomXD int online_cloud_timeout_ms
        self.notify_cloud_delay_ms = notify_cloud_delay_ms  # t.me/TheVenomXD int notify_default_delay_ms
        self.push_chat_period_ms = push_chat_period_ms  # t.me/TheVenomXD int push_chat_limit
        self.saved_gifs_limit = saved_gifs_limit  # t.me/TheVenomXD int edit_time_limit
        self.revoke_time_limit = revoke_time_limit  # t.me/TheVenomXD int revoke_pm_time_limit
        self.rating_e_decay = rating_e_decay  # t.me/TheVenomXD int stickers_recent_limit
        self.stickers_faved_limit = stickers_faved_limit  # t.me/TheVenomXD int channels_read_media_period
        self.pinned_infolder_count_max = pinned_infolder_count_max  # t.me/TheVenomXD int call_receive_timeout_ms
        self.call_ring_timeout_ms = call_ring_timeout_ms  # t.me/TheVenomXD int call_connect_timeout_ms
        self.call_packet_timeout_ms = call_packet_timeout_ms  # t.me/TheVenomXD int me_url_prefix
        self.message_length_max = message_length_max  # t.me/TheVenomXD int webfile_octra_dc_id_
        self.default_p2p_contacts = default_p2p_contacts  # t.me/TheVenomXD flags.3?true preload_featured_stickers
        self.ignore_phone_entities = ignore_phone_entities  # t.me/TheVenomXD flags.5?true revoke_pm_inbox
        self.blocked_mode = blocked_mode  # t.me/TheVenomXD flags.8?true pfs_enabled
        self.force_try_ipv6 = force_try_ipv6  # t.me/TheVenomXD flags.14?true date
        self.tmp_sessions = tmp_sessions  # t.me/TheVenomXD flags.0?int pinned_dialogs_count_max
        self.autoupdate_url_prefix = autoupdate_url_prefix  # t.me/TheVenomXD flags.7?string gif_search_username
        self.venue_search_username = venue_search_username  # t.me/TheVenomXD flags.10?string img_search_username
        self.static_maps_provider = static_maps_provider  # t.me/TheVenomXD flags.12?string caption_length_max
        self.suggested_lang_code = suggested_lang_code  # t.me/TheVenomXD flags.2?string lang_pack_version
        self.base_lang_pack_version = base_lang_pack_version  # t.me/TheVenomXD flags.2?int reactions_default

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Config":
        
        flags = TLObject.read(b)
        
        default_p2p_contacts = True if flags & (1 << 3) else False
        ignore_phone_entities = True if flags & (1 << 5) else False
        blocked_mode = True if flags & (1 << 8) else False
        force_try_ipv6 = True if flags & (1 << 14) else False
        expires = TLObject.read(b)
        
        this_dc = TLObject.read(b)
        
        dc_txt_domain_name = TLObject.read(b)
        
        megagroup_size_max = TLObject.read(b)
        
        online_update_period_ms = TLObject.read(b)
        
        offline_idle_timeout_ms = TLObject.read(b)
        
        notify_cloud_delay_ms = TLObject.read(b)
        
        push_chat_period_ms = TLObject.read(b)
        
        saved_gifs_limit = TLObject.read(b)
        
        revoke_time_limit = TLObject.read(b)
        
        rating_e_decay = TLObject.read(b)
        
        stickers_faved_limit = TLObject.read(b)
        
        tmp_sessions = Int.read(b) if flags & (1 << 0) else None
        pinned_infolder_count_max = TLObject.read(b)
        
        call_ring_timeout_ms = TLObject.read(b)
        
        call_packet_timeout_ms = TLObject.read(b)
        
        autoupdate_url_prefix = String.read(b) if flags & (1 << 7) else None
        venue_search_username = String.read(b) if flags & (1 << 10) else None
        static_maps_provider = String.read(b) if flags & (1 << 12) else None
        message_length_max = TLObject.read(b)
        
        suggested_lang_code = String.read(b) if flags & (1 << 2) else None
        base_lang_pack_version = Int.read(b) if flags & (1 << 2) else None
        return Config(flags=flags, expires=expires, this_dc=this_dc, dc_txt_domain_name=dc_txt_domain_name, megagroup_size_max=megagroup_size_max, online_update_period_ms=online_update_period_ms, offline_idle_timeout_ms=offline_idle_timeout_ms, notify_cloud_delay_ms=notify_cloud_delay_ms, push_chat_period_ms=push_chat_period_ms, saved_gifs_limit=saved_gifs_limit, revoke_time_limit=revoke_time_limit, rating_e_decay=rating_e_decay, stickers_faved_limit=stickers_faved_limit, pinned_infolder_count_max=pinned_infolder_count_max, call_ring_timeout_ms=call_ring_timeout_ms, call_packet_timeout_ms=call_packet_timeout_ms, message_length_max=message_length_max, default_p2p_contacts=default_p2p_contacts, ignore_phone_entities=ignore_phone_entities, blocked_mode=blocked_mode, force_try_ipv6=force_try_ipv6, tmp_sessions=tmp_sessions, autoupdate_url_prefix=autoupdate_url_prefix, venue_search_username=venue_search_username, static_maps_provider=static_maps_provider, suggested_lang_code=suggested_lang_code, base_lang_pack_version=base_lang_pack_version)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(self.flags.write())
        
        b.write(self.expires.write())
        
        b.write(self.this_dc.write())
        
        b.write(self.dc_txt_domain_name.write())
        
        b.write(self.megagroup_size_max.write())
        
        b.write(self.online_update_period_ms.write())
        
        b.write(self.offline_idle_timeout_ms.write())
        
        b.write(self.notify_cloud_delay_ms.write())
        
        b.write(self.push_chat_period_ms.write())
        
        b.write(self.saved_gifs_limit.write())
        
        b.write(self.revoke_time_limit.write())
        
        b.write(self.rating_e_decay.write())
        
        b.write(self.stickers_faved_limit.write())
        
        if self.tmp_sessions is not None:
            b.write(Int(self.tmp_sessions))
        
        b.write(self.pinned_infolder_count_max.write())
        
        b.write(self.call_ring_timeout_ms.write())
        
        b.write(self.call_packet_timeout_ms.write())
        
        if self.autoupdate_url_prefix is not None:
            b.write(String(self.autoupdate_url_prefix))
        
        if self.venue_search_username is not None:
            b.write(String(self.venue_search_username))
        
        if self.static_maps_provider is not None:
            b.write(String(self.static_maps_provider))
        
        b.write(self.message_length_max.write())
        
        if self.suggested_lang_code is not None:
            b.write(String(self.suggested_lang_code))
        
        if self.base_lang_pack_version is not None:
            b.write(Int(self.base_lang_pack_version))
        
        return b.getvalue()
