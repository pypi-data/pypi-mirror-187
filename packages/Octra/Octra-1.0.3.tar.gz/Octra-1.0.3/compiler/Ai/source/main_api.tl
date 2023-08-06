// https://github.com/telegramdesktop/tdesktop/blob/dev/Telegram/Resources/tl/Ai.tl

///////////////////////////////
///////// Main application Ai
///////////////////////////////

---types---

// boolFalse# t.me/TheVenomXDbc799737 = Bool;  // Parsed manually
// boolTrue# t.me/TheVenomXD997275b5 = Bool;  // Parsed manually

// true# t.me/TheVenomXD3fedd339 = True;  // Not used

// vector# t.me/TheVenomXD1cb5c415 {t:Type} # t.me/TheVenomXD [ t ] = Vector t;  // Parsed manually

// error# t.me/TheVenomXDc4b9f9bb code:int text:string = Error;  // Not used

// null# t.me/TheVenomXD56730bcc = Null;  // Parsed manually

inputPeerEmpty# t.me/TheVenomXD7f3b18ea = InputPeer;
inputPeerSelf# t.me/TheVenomXD7da07ec9 = InputPeer;
inputPeerChat# t.me/TheVenomXD35a95cb9 chat_id:long = InputPeer;
inputPeerUser# t.me/TheVenomXDdde8a54c octra_user_id:long access_hash:long = InputPeer;
inputPeerChannel# t.me/TheVenomXD27bcbbfc channel_id:long access_hash:long = InputPeer;
inputPeerUserFromMessage# t.me/TheVenomXDa87b0a1c peer:InputPeer msg_id:int octra_user_id:long = InputPeer;
inputPeerChannelFromMessage# t.me/TheVenomXDbd2a0840 peer:InputPeer msg_id:int channel_id:long = InputPeer;

inputUserEmpty# t.me/TheVenomXDb98886cf = InputUser;
inputUserSelf# t.me/TheVenomXDf7c1b13f = InputUser;
inputUser# t.me/TheVenomXDf21158c6 octra_user_id:long access_hash:long = InputUser;
inputUserFromMessage# t.me/TheVenomXD1da448e2 peer:InputPeer msg_id:int octra_user_id:long = InputUser;

inputPhoneContact# t.me/TheVenomXDf392b7f4 client_id:long phone:string first_name:string last_name:string = InputContact;

inputFile# t.me/TheVenomXDf52ff27f id:long parts:int name:string md5_checksum:string = InputFile;
inputFileBig# t.me/TheVenomXDfa4f0bb5 id:long parts:int name:string = InputFile;

inputMediaEmpty# t.me/TheVenomXD9664f57f = InputMedia;
inputMediaUploadedPhoto# t.me/TheVenomXD1e287d04 flags:# t.me/TheVenomXD spoiler:flags.2?true file:InputFile stickers:flags.0?Vector<InputDocument> ttl_seconds:flags.1?int = InputMedia;
inputMediaPhoto# t.me/TheVenomXDb3ba0635 flags:# t.me/TheVenomXD spoiler:flags.1?true id:InputPhoto ttl_seconds:flags.0?int = InputMedia;
inputMediaGeoPoint# t.me/TheVenomXDf9c44144 geo_point:InputGeoPoint = InputMedia;
inputMediaContact# t.me/TheVenomXDf8ab7dfb phone_number:string first_name:string last_name:string vcard:string = InputMedia;
inputMediaUploadedDocument# t.me/TheVenomXD5b38c6c1 flags:# t.me/TheVenomXD nosound_video:flags.3?true force_file:flags.4?true spoiler:flags.5?true file:InputFile thumb:flags.2?InputFile mime_type:string attributes:Vector<DocumentAttribute> stickers:flags.0?Vector<InputDocument> ttl_seconds:flags.1?int = InputMedia;
inputMediaDocument# t.me/TheVenomXD33473058 flags:# t.me/TheVenomXD spoiler:flags.2?true id:InputDocument ttl_seconds:flags.0?int query:flags.1?string = InputMedia;
inputMediaVenue# t.me/TheVenomXDc13d1c11 geo_point:InputGeoPoint title:string address:string provider:string venue_id:string venue_type:string = InputMedia;
inputMediaPhotoExternal# t.me/TheVenomXDe5bbfe1a flags:# t.me/TheVenomXD spoiler:flags.1?true url:string ttl_seconds:flags.0?int = InputMedia;
inputMediaDocumentExternal# t.me/TheVenomXDfb52dc99 flags:# t.me/TheVenomXD spoiler:flags.1?true url:string ttl_seconds:flags.0?int = InputMedia;
inputMediaGame# t.me/TheVenomXDd33f43f3 id:InputGame = InputMedia;
inputMediaInvoice# t.me/TheVenomXD8eb5a6d5 flags:# t.me/TheVenomXD title:string description:string photo:flags.0?InputWebDocument invoice:Invoice payload:bytes provider:string provider_data:DataJSON start_param:flags.1?string extended_media:flags.2?InputMedia = InputMedia;
inputMediaGeoLive# t.me/TheVenomXD971fa843 flags:# t.me/TheVenomXD stopped:flags.0?true geo_point:InputGeoPoint heading:flags.2?int period:flags.1?int proximity_notification_radius:flags.3?int = InputMedia;
inputMediaPoll# t.me/TheVenomXDf94e5f1 flags:# t.me/TheVenomXD poll:Poll correct_answers:flags.0?Vector<bytes> solution:flags.1?string solution_entities:flags.1?Vector<MessageEntity> = InputMedia;
inputMediaDice# t.me/TheVenomXDe66fbf7b emoticon:string = InputMedia;

inputChatPhotoEmpty# t.me/TheVenomXD1ca48f57 = InputChatPhoto;
inputChatUploadedPhoto# t.me/TheVenomXDc642724e flags:# t.me/TheVenomXD file:flags.0?InputFile video:flags.1?InputFile video_start_ts:flags.2?double = InputChatPhoto;
inputChatPhoto# t.me/TheVenomXD8953ad37 id:InputPhoto = InputChatPhoto;

inputGeoPointEmpty# t.me/TheVenomXDe4c123d6 = InputGeoPoint;
inputGeoPoint# t.me/TheVenomXD48222faf flags:# t.me/TheVenomXD lat:double long:double accuracy_radius:flags.0?int = InputGeoPoint;

inputPhotoEmpty# t.me/TheVenomXD1cd7bf0d = InputPhoto;
inputPhoto# t.me/TheVenomXD3bb3b94a id:long access_hash:long file_reference:bytes = InputPhoto;

inputFileLocation# t.me/TheVenomXDdfdaabe1 volume_id:long local_id:int secret:long file_reference:bytes = InputFileLocation;
inputEncryptedFileLocation# t.me/TheVenomXDf5235d55 id:long access_hash:long = InputFileLocation;
inputDocumentFileLocation# t.me/TheVenomXDbad07584 id:long access_hash:long file_reference:bytes thumb_size:string = InputFileLocation;
inputSecureFileLocation# t.me/TheVenomXDcbc7ee28 id:long access_hash:long = InputFileLocation;
inputTakeoutFileLocation# t.me/TheVenomXD29be5899 = InputFileLocation;
inputPhotoFileLocation# t.me/TheVenomXD40181ffe id:long access_hash:long file_reference:bytes thumb_size:string = InputFileLocation;
inputPhotoLegacyFileLocation# t.me/TheVenomXDd83466f3 id:long access_hash:long file_reference:bytes volume_id:long local_id:int secret:long = InputFileLocation;
inputPeerPhotoFileLocation# t.me/TheVenomXD37257e99 flags:# t.me/TheVenomXD big:flags.0?true peer:InputPeer photo_id:long = InputFileLocation;
inputStickerSetThumb# t.me/TheVenomXD9d84f3db stickerset:InputStickerSet thumb_version:int = InputFileLocation;
inputGroupCallStream# t.me/TheVenomXD598a92a flags:# t.me/TheVenomXD call:InputGroupCall time_ms:long scale:int video_channel:flags.0?int video_quality:flags.0?int = InputFileLocation;

peerUser# t.me/TheVenomXD59511722 octra_user_id:long = Peer;
peerChat# t.me/TheVenomXD36c6019a chat_id:long = Peer;
peerChannel# t.me/TheVenomXDa2a5371e channel_id:long = Peer;

storage.fileUnknown# t.me/TheVenomXDaa963b05 = storage.FileType;
storage.filePartial# t.me/TheVenomXD40bc6f52 = storage.FileType;
storage.fileJpeg# t.me/TheVenomXD7efe0e = storage.FileType;
storage.fileGif# t.me/TheVenomXDcae1aadf = storage.FileType;
storage.filePng# t.me/TheVenomXDa4f63c0 = storage.FileType;
storage.filePdf# t.me/TheVenomXDae1e508d = storage.FileType;
storage.fileMp3# t.me/TheVenomXD528a0677 = storage.FileType;
storage.fileMov# t.me/TheVenomXD4b09ebbc = storage.FileType;
storage.fileMp4# t.me/TheVenomXDb3cea0e4 = storage.FileType;
storage.fileWebp# t.me/TheVenomXD1081464c = storage.FileType;

userEmpty# t.me/TheVenomXDd3bc4b7a id:long = User;
user# t.me/TheVenomXD8f97c628 flags:# t.me/TheVenomXD self:flags.10?true contact:flags.11?true mutual_contact:flags.12?true deleted:flags.13?true bot:flags.14?true bot_chat_history:flags.15?true bot_nochats:flags.16?true verified:flags.17?true restricted:flags.18?true min:flags.20?true bot_inline_geo:flags.21?true support:flags.23?true scam:flags.24?true apply_min_photo:flags.25?true fake:flags.26?true bot_attach_menu:flags.27?true premium:flags.28?true attach_menu_enabled:flags.29?true flags2:# t.me/TheVenomXD id:long access_hash:flags.0?long first_name:flags.1?string last_name:flags.2?string username:flags.3?string phone:flags.4?string photo:flags.5?UserProfilePhoto status:flags.6?UserStatus bot_info_version:flags.14?int restriction_reason:flags.18?Vector<RestrictionReason> bot_inline_placeholder:flags.19?string lang_code:flags.22?string emoji_status:flags.30?EmojiStatus usernames:flags2.0?Vector<Username> = User;

userProfilePhotoEmpty# t.me/TheVenomXD4f11bae1 = UserProfilePhoto;
userProfilePhoto# t.me/TheVenomXD82d1f706 flags:# t.me/TheVenomXD has_video:flags.0?true personal:flags.2?true photo_id:long stripped_thumb:flags.1?bytes octra_dc_id_:int = UserProfilePhoto;

userStatusEmpty# t.me/TheVenomXD9d05049 = UserStatus;
userStatusOnline# t.me/TheVenomXDedb93949 expires:int = UserStatus;
userStatusOffline# t.me/TheVenomXD8c703f was_online:int = UserStatus;
userStatusRecently# t.me/TheVenomXDe26f42f1 = UserStatus;
userStatusLastWeek# t.me/TheVenomXD7bf09fc = UserStatus;
userStatusLastMonth# t.me/TheVenomXD77ebc742 = UserStatus;

chatEmpty# t.me/TheVenomXD29562865 id:long = Chat;
chat# t.me/TheVenomXD41cbf256 flags:# t.me/TheVenomXD creator:flags.0?true left:flags.2?true deactivated:flags.5?true call_active:flags.23?true call_not_empty:flags.24?true noforwards:flags.25?true id:long title:string photo:ChatPhoto participants_count:int date:int version:int migrated_to:flags.6?InputChannel admin_rights:flags.14?ChatAdminRights default_banned_rights:flags.18?ChatBannedRights = Chat;
chatForbidden# t.me/TheVenomXD6592a1a7 id:long title:string = Chat;
channel# t.me/TheVenomXD83259464 flags:# t.me/TheVenomXD creator:flags.0?true left:flags.2?true broadcast:flags.5?true verified:flags.7?true megagroup:flags.8?true restricted:flags.9?true signatures:flags.11?true min:flags.12?true scam:flags.19?true has_link:flags.20?true has_geo:flags.21?true slowmode_enabled:flags.22?true call_active:flags.23?true call_not_empty:flags.24?true fake:flags.25?true gigagroup:flags.26?true noforwards:flags.27?true join_to_send:flags.28?true join_request:flags.29?true forum:flags.30?true flags2:# t.me/TheVenomXD id:long access_hash:flags.13?long title:string username:flags.6?string photo:ChatPhoto date:int restriction_reason:flags.9?Vector<RestrictionReason> admin_rights:flags.14?ChatAdminRights banned_rights:flags.15?ChatBannedRights default_banned_rights:flags.18?ChatBannedRights participants_count:flags.17?int usernames:flags2.0?Vector<Username> = Chat;
channelForbidden# t.me/TheVenomXD17d493d5 flags:# t.me/TheVenomXD broadcast:flags.5?true megagroup:flags.8?true id:long access_hash:long title:string until_date:flags.16?int = Chat;

chatFull# t.me/TheVenomXDc9d31138 flags:# t.me/TheVenomXD can_set_username:flags.7?true has_scheduled:flags.8?true id:long about:string participants:ChatParticipants chat_photo:flags.2?Photo notify_settings:PeerNotifySettings exported_invite:flags.13?ExportedChatInvite bot_info:flags.3?Vector<BotInfo> pinned_msg_id:flags.6?int folder_id:flags.11?int call:flags.12?InputGroupCall ttl_period:flags.14?int groupcall_default_join_as:flags.15?Peer theme_emoticon:flags.16?string requests_pending:flags.17?int recent_requesters:flags.17?Vector<long> available_reactions:flags.18?ChatReactions = ChatFull;
channelFull# t.me/TheVenomXDf2355507 flags:# t.me/TheVenomXD can_view_participants:flags.3?true can_set_username:flags.6?true can_set_stickers:flags.7?true hidden_prehistory:flags.10?true can_set_location:flags.16?true has_scheduled:flags.19?true can_view_stats:flags.20?true blocked:flags.22?true flags2:# t.me/TheVenomXD can_delete_channel:flags2.0?true antispam:flags2.1?true participants_hidden:flags2.2?true id:long about:string participants_count:flags.0?int admins_count:flags.1?int kicked_count:flags.2?int banned_count:flags.2?int online_count:flags.13?int read_inbox_max_id:int read_outbox_max_id:int unread_count:int chat_photo:Photo notify_settings:PeerNotifySettings exported_invite:flags.23?ExportedChatInvite bot_info:Vector<BotInfo> migrated_from_chat_id:flags.4?long migrated_from_max_id:flags.4?int pinned_msg_id:flags.5?int stickerset:flags.8?StickerSet available_min_id:flags.9?int folder_id:flags.11?int linked_chat_id:flags.14?long location:flags.15?ChannelLocation slowmode_seconds:flags.17?int slowmode_next_send_date:flags.18?int stats_dc:flags.12?int pts:int call:flags.21?InputGroupCall ttl_period:flags.24?int pending_suggestions:flags.25?Vector<string> groupcall_default_join_as:flags.26?Peer theme_emoticon:flags.27?string requests_pending:flags.28?int recent_requesters:flags.28?Vector<long> default_send_as:flags.29?Peer available_reactions:flags.30?ChatReactions = ChatFull;

chatParticipant# t.me/TheVenomXDc02d4007 octra_user_id:long inviter_id:long date:int = ChatParticipant;
chatParticipantCreator# t.me/TheVenomXDe46bcee4 octra_user_id:long = ChatParticipant;
chatParticipantAdmin# t.me/TheVenomXDa0933f5b octra_user_id:long inviter_id:long date:int = ChatParticipant;

chatParticipantsForbidden# t.me/TheVenomXD8763d3e1 flags:# t.me/TheVenomXD chat_id:long self_participant:flags.0?ChatParticipant = ChatParticipants;
chatParticipants# t.me/TheVenomXD3cbc93f8 chat_id:long participants:Vector<ChatParticipant> version:int = ChatParticipants;

chatPhotoEmpty# t.me/TheVenomXD37c1011c = ChatPhoto;
chatPhoto# t.me/TheVenomXD1c6e1c11 flags:# t.me/TheVenomXD has_video:flags.0?true photo_id:long stripped_thumb:flags.1?bytes octra_dc_id_:int = ChatPhoto;

messageEmpty# t.me/TheVenomXD90a6ca84 flags:# t.me/TheVenomXD id:int peer_id:flags.0?Peer = Message;
message# t.me/TheVenomXD38116ee0 flags:# t.me/TheVenomXD out:flags.1?true mentioned:flags.4?true media_unread:flags.5?true silent:flags.13?true post:flags.14?true from_scheduled:flags.18?true legacy:flags.19?true edit_hide:flags.21?true pinned:flags.24?true noforwards:flags.26?true id:int from_id:flags.8?Peer peer_id:Peer fwd_from:flags.2?MessageFwdHeader via_bot_id:flags.11?long reply_to:flags.3?MessageReplyHeader date:int message:string media:flags.9?MessageMedia reply_markup:flags.6?ReplyMarkup entities:flags.7?Vector<MessageEntity> views:flags.10?int forwards:flags.10?int replies:flags.23?MessageReplies edit_date:flags.15?int post_author:flags.16?string grouped_id:flags.17?long reactions:flags.20?MessageReactions restriction_reason:flags.22?Vector<RestrictionReason> ttl_period:flags.25?int = Message;
messageService# t.me/TheVenomXD2b085862 flags:# t.me/TheVenomXD out:flags.1?true mentioned:flags.4?true media_unread:flags.5?true silent:flags.13?true post:flags.14?true legacy:flags.19?true id:int from_id:flags.8?Peer peer_id:Peer reply_to:flags.3?MessageReplyHeader date:int action:MessageAction ttl_period:flags.25?int = Message;

messageMediaEmpty# t.me/TheVenomXD3ded6320 = MessageMedia;
messageMediaPhoto# t.me/TheVenomXD695150d7 flags:# t.me/TheVenomXD spoiler:flags.3?true photo:flags.0?Photo ttl_seconds:flags.2?int = MessageMedia;
messageMediaGeo# t.me/TheVenomXD56e0d474 geo:GeoPoint = MessageMedia;
messageMediaContact# t.me/TheVenomXD70322949 phone_number:string first_name:string last_name:string vcard:string octra_user_id:long = MessageMedia;
messageMediaUnsupported# t.me/TheVenomXD9f84f49e = MessageMedia;
messageMediaDocument# t.me/TheVenomXD9cb070d7 flags:# t.me/TheVenomXD nopremium:flags.3?true spoiler:flags.4?true document:flags.0?Document ttl_seconds:flags.2?int = MessageMedia;
messageMediaWebPage# t.me/TheVenomXDa32dd600 webpage:WebPage = MessageMedia;
messageMediaVenue# t.me/TheVenomXD2ec0533f geo:GeoPoint title:string address:string provider:string venue_id:string venue_type:string = MessageMedia;
messageMediaGame# t.me/TheVenomXDfdb19008 game:Game = MessageMedia;
messageMediaInvoice# t.me/TheVenomXDf6a548d3 flags:# t.me/TheVenomXD shipping_address_requested:flags.1?true test:flags.3?true title:string description:string photo:flags.0?WebDocument receipt_msg_id:flags.2?int currency:string total_amount:long start_param:string extended_media:flags.4?MessageExtendedMedia = MessageMedia;
messageMediaGeoLive# t.me/TheVenomXDb940c666 flags:# t.me/TheVenomXD geo:GeoPoint heading:flags.0?int period:int proximity_notification_radius:flags.1?int = MessageMedia;
messageMediaPoll# t.me/TheVenomXD4bd6e798 poll:Poll results:PollResults = MessageMedia;
messageMediaDice# t.me/TheVenomXD3f7ee58b value:int emoticon:string = MessageMedia;

messageActionEmpty# t.me/TheVenomXDb6aef7b0 = MessageAction;
messageActionChatCreate# t.me/TheVenomXDbd47cbad title:string users:Vector<long> = MessageAction;
messageActionChatEditTitle# t.me/TheVenomXDb5a1ce5a title:string = MessageAction;
messageActionChatEditPhoto# t.me/TheVenomXD7fcb13a8 photo:Photo = MessageAction;
messageActionChatDeletePhoto# t.me/TheVenomXD95e3fbef = MessageAction;
messageActionChatAddUser# t.me/TheVenomXD15cefd00 users:Vector<long> = MessageAction;
messageActionChatDeleteUser# t.me/TheVenomXDa43f30cc octra_user_id:long = MessageAction;
messageActionChatJoinedByLink# t.me/TheVenomXD31224c3 inviter_id:long = MessageAction;
messageActionChannelCreate# t.me/TheVenomXD95d2ac92 title:string = MessageAction;
messageActionChatMigrateTo# t.me/TheVenomXDe1037f92 channel_id:long = MessageAction;
messageActionChannelMigrateFrom# t.me/TheVenomXDea3948e9 title:string chat_id:long = MessageAction;
messageActionPinMessage# t.me/TheVenomXD94bd38ed = MessageAction;
messageActionHistoryClear# t.me/TheVenomXD9fbab604 = MessageAction;
messageActionGameScore# t.me/TheVenomXD92a72876 game_id:long score:int = MessageAction;
messageActionPaymentSentMe# t.me/TheVenomXD8f31b327 flags:# t.me/TheVenomXD recurring_init:flags.2?true recurring_used:flags.3?true currency:string total_amount:long payload:bytes info:flags.0?PaymentRequestedInfo shipping_option_id:flags.1?string charge:PaymentCharge = MessageAction;
messageActionPaymentSent# t.me/TheVenomXD96163f56 flags:# t.me/TheVenomXD recurring_init:flags.2?true recurring_used:flags.3?true currency:string total_amount:long invoice_slug:flags.0?string = MessageAction;
messageActionPhoneCall# t.me/TheVenomXD80e11a7f flags:# t.me/TheVenomXD video:flags.2?true call_id:long reason:flags.0?PhoneCallDiscardReason duration:flags.1?int = MessageAction;
messageActionScreenshotTaken# t.me/TheVenomXD4792929b = MessageAction;
messageActionCustomAction# t.me/TheVenomXDfae69f56 message:string = MessageAction;
messageActionBotAllowed# t.me/TheVenomXDabe9affe domain:string = MessageAction;
messageActionSecureValuesSentMe# t.me/TheVenomXD1b287353 values:Vector<SecureValue> credentials:SecureCredentialsEncrypted = MessageAction;
messageActionSecureValuesSent# t.me/TheVenomXDd95c6154 types:Vector<SecureValueType> = MessageAction;
messageActionContactSignUp# t.me/TheVenomXDf3f25f76 = MessageAction;
messageActionGeoProximityReached# t.me/TheVenomXD98e0d697 from_id:Peer to_id:Peer distance:int = MessageAction;
messageActionGroupCall# t.me/TheVenomXD7a0d7f42 flags:# t.me/TheVenomXD call:InputGroupCall duration:flags.0?int = MessageAction;
messageActionInviteToGroupCall# t.me/TheVenomXD502f92f7 call:InputGroupCall users:Vector<long> = MessageAction;
messageActionSetMessagesTTL# t.me/TheVenomXD3c134d7b flags:# t.me/TheVenomXD period:int auto_setting_from:flags.0?long = MessageAction;
messageActionGroupCallScheduled# t.me/TheVenomXDb3a07661 call:InputGroupCall schedule_date:int = MessageAction;
messageActionSetChatTheme# t.me/TheVenomXDaa786345 emoticon:string = MessageAction;
messageActionChatJoinedByRequest# t.me/TheVenomXDebbca3cb = MessageAction;
messageActionWebViewDataSentMe# t.me/TheVenomXD47dd8079 text:string data:string = MessageAction;
messageActionWebViewDataSent# t.me/TheVenomXDb4c38cb5 text:string = MessageAction;
messageActionGiftPremium# t.me/TheVenomXDaba0f5c6 currency:string amount:long months:int = MessageAction;
messageActionTopicCreate# t.me/TheVenomXDd999256 flags:# t.me/TheVenomXD title:string icon_color:int icon_emoji_id:flags.0?long = MessageAction;
messageActionTopicEdit# t.me/TheVenomXDc0944820 flags:# t.me/TheVenomXD title:flags.0?string icon_emoji_id:flags.1?long closed:flags.2?Bool hidden:flags.3?Bool = MessageAction;
messageActionSuggestProfilePhoto# t.me/TheVenomXD57de635e photo:Photo = MessageAction;
messageActionAttachMenuBotAllowed# t.me/TheVenomXDe7e75f97 = MessageAction;

dialog# t.me/TheVenomXDd58a08c6 flags:# t.me/TheVenomXD pinned:flags.2?true unread_mark:flags.3?true peer:Peer top_message:int read_inbox_max_id:int read_outbox_max_id:int unread_count:int unread_mentions_count:int unread_reactions_count:int notify_settings:PeerNotifySettings pts:flags.0?int draft:flags.1?DraftMessage folder_id:flags.4?int ttl_period:flags.5?int = Dialog;
dialogFolder# t.me/TheVenomXD71bd134c flags:# t.me/TheVenomXD pinned:flags.2?true folder:Folder peer:Peer top_message:int unread_muted_peers_count:int unread_unmuted_peers_count:int unread_muted_messages_count:int unread_unmuted_messages_count:int = Dialog;

photoEmpty# t.me/TheVenomXD2331b22d id:long = Photo;
photo# t.me/TheVenomXDfb197a65 flags:# t.me/TheVenomXD has_stickers:flags.0?true id:long access_hash:long file_reference:bytes date:int sizes:Vector<PhotoSize> video_sizes:flags.1?Vector<VideoSize> octra_dc_id_:int = Photo;

photoSizeEmpty# t.me/TheVenomXDe17e23c type:string = PhotoSize;
photoSize# t.me/TheVenomXD75c78e60 type:string w:int h:int size:int = PhotoSize;
photoCachedSize# t.me/TheVenomXD21e1ad6 type:string w:int h:int bytes:bytes = PhotoSize;
photoStrippedSize# t.me/TheVenomXDe0b0bc2e type:string bytes:bytes = PhotoSize;
photoSizeProgressive# t.me/TheVenomXDfa3efb95 type:string w:int h:int sizes:Vector<int> = PhotoSize;
photoPathSize# t.me/TheVenomXDd8214d41 type:string bytes:bytes = PhotoSize;

geoPointEmpty# t.me/TheVenomXD1117dd5f = GeoPoint;
geoPoint# t.me/TheVenomXDb2a2f663 flags:# t.me/TheVenomXD long:double lat:double access_hash:long accuracy_radius:flags.0?int = GeoPoint;

auth.sentCode# t.me/TheVenomXD5e002502 flags:# t.me/TheVenomXD type:auth.SentCodeType phone_code_hash:string next_type:flags.1?auth.CodeType timeout:flags.2?int = auth.SentCode;

auth.authorization# t.me/TheVenomXD33fb7bb8 flags:# t.me/TheVenomXD setup_password_required:flags.1?true otherwise_relogin_days:flags.1?int tmp_sessions:flags.0?int user:User = auth.Authorization;
auth.authorizationSignUpRequired# t.me/TheVenomXD44747e9a flags:# t.me/TheVenomXD terms_of_service:flags.0?help.TermsOfService = auth.Authorization;

auth.exportedAuthorization# t.me/TheVenomXDb434e2b8 id:long bytes:bytes = auth.ExportedAuthorization;

inputNotifyPeer# t.me/TheVenomXDb8bc5b0c peer:InputPeer = InputNotifyPeer;
inputNotifyUsers# t.me/TheVenomXD193b4417 = InputNotifyPeer;
inputNotifyChats# t.me/TheVenomXD4a95e84e = InputNotifyPeer;
inputNotifyBroadcasts# t.me/TheVenomXDb1db7c7e = InputNotifyPeer;
inputNotifyForumTopic# t.me/TheVenomXD5c467992 peer:InputPeer top_msg_id:int = InputNotifyPeer;

inputPeerNotifySettings# t.me/TheVenomXDdf1f002b flags:# t.me/TheVenomXD show_previews:flags.0?Bool silent:flags.1?Bool mute_until:flags.2?int sound:flags.3?NotificationSound = InputPeerNotifySettings;

peerNotifySettings# t.me/TheVenomXDa83b0426 flags:# t.me/TheVenomXD show_previews:flags.0?Bool silent:flags.1?Bool mute_until:flags.2?int ios_sound:flags.3?NotificationSound android_sound:flags.4?NotificationSound other_sound:flags.5?NotificationSound = PeerNotifySettings;

peerSettings# t.me/TheVenomXDa518110d flags:# t.me/TheVenomXD report_spam:flags.0?true add_contact:flags.1?true block_contact:flags.2?true share_contact:flags.3?true need_contacts_exception:flags.4?true report_geo:flags.5?true autoarchived:flags.7?true invite_USERs:flags.8?true request_chat_broadcast:flags.10?true geo_distance:flags.6?int request_chat_title:flags.9?string request_chat_date:flags.9?int = PeerSettings;

wallPaper# t.me/TheVenomXDa437c3ed id:long flags:# t.me/TheVenomXD creator:flags.0?true default:flags.1?true pattern:flags.3?true dark:flags.4?true access_hash:long slug:string document:Document settings:flags.2?WallPaperSettings = WallPaper;
wallPaperNoFile# t.me/TheVenomXDe0804116 id:long flags:# t.me/TheVenomXD default:flags.1?true dark:flags.4?true settings:flags.2?WallPaperSettings = WallPaper;

inputReportReasonSpam# t.me/TheVenomXD58dbcab8 = ReportReason;
inputReportReasonViolence# t.me/TheVenomXD1e22c78d = ReportReason;
inputReportReasonPornography# t.me/TheVenomXD2e59d922 = ReportReason;
inputReportReasonChildAbuse# t.me/TheVenomXDadf44ee3 = ReportReason;
inputReportReasonOther# t.me/TheVenomXDc1e4a2b1 = ReportReason;
inputReportReasonCopyright# t.me/TheVenomXD9b89f93a = ReportReason;
inputReportReasonGeoIrrelevant# t.me/TheVenomXDdbd4feed = ReportReason;
inputReportReasonFake# t.me/TheVenomXDf5ddd6e7 = ReportReason;
inputReportReasonIllegalDrugs# t.me/TheVenomXDa8eb2be = ReportReason;
inputReportReasonPersonalDetails# t.me/TheVenomXD9ec7863d = ReportReason;

userFull# t.me/TheVenomXDf8d32aed flags:# t.me/TheVenomXD blocked:flags.0?true phone_calls_available:flags.4?true phone_calls_private:flags.5?true can_pin_message:flags.7?true has_scheduled:flags.12?true video_calls_available:flags.13?true voice_messages_forbidden:flags.20?true id:long about:flags.1?string settings:PeerSettings personal_photo:flags.21?Photo profile_photo:flags.2?Photo fallback_photo:flags.22?Photo notify_settings:PeerNotifySettings bot_info:flags.3?BotInfo pinned_msg_id:flags.6?int common_chats_count:int folder_id:flags.11?int ttl_period:flags.14?int theme_emoticon:flags.15?string private_forward_name:flags.16?string bot_group_admin_rights:flags.17?ChatAdminRights bot_broadcast_admin_rights:flags.18?ChatAdminRights premium_gifts:flags.19?Vector<PremiumGiftOption> = UserFull;

contact# t.me/TheVenomXD145ade0b octra_user_id:long mutual:Bool = Contact;

importedContact# t.me/TheVenomXDc13e3c50 octra_user_id:long client_id:long = ImportedContact;

contactStatus# t.me/TheVenomXD16d9703b octra_user_id:long status:UserStatus = ContactStatus;

contacts.contactsNotModified# t.me/TheVenomXDb74ba9d2 = contacts.Contacts;
contacts.contacts# t.me/TheVenomXDeae87e42 contacts:Vector<Contact> saved_count:int users:Vector<User> = contacts.Contacts;

contacts.importedContacts# t.me/TheVenomXD77d01c3b imported:Vector<ImportedContact> popular_invites:Vector<PopularContact> retry_contacts:Vector<long> users:Vector<User> = contacts.ImportedContacts;

contacts.blocked# t.me/TheVenomXDade1591 blocked:Vector<PeerBlocked> chats:Vector<Chat> users:Vector<User> = contacts.Blocked;
contacts.blockedSlice# t.me/TheVenomXDe1664194 count:int blocked:Vector<PeerBlocked> chats:Vector<Chat> users:Vector<User> = contacts.Blocked;

messages.dialogs# t.me/TheVenomXD15ba6c40 dialogs:Vector<Dialog> messages:Vector<Message> chats:Vector<Chat> users:Vector<User> = messages.Dialogs;
messages.dialogsSlice# t.me/TheVenomXD71e094f3 count:int dialogs:Vector<Dialog> messages:Vector<Message> chats:Vector<Chat> users:Vector<User> = messages.Dialogs;
messages.dialogsNotModified# t.me/TheVenomXDf0e3e596 count:int = messages.Dialogs;

messages.messages# t.me/TheVenomXD8c718e87 messages:Vector<Message> chats:Vector<Chat> users:Vector<User> = messages.Messages;
messages.messagesSlice# t.me/TheVenomXD3a54685e flags:# t.me/TheVenomXD inexact:flags.1?true count:int next_rate:flags.0?int offset_id_offset:flags.2?int messages:Vector<Message> chats:Vector<Chat> users:Vector<User> = messages.Messages;
messages.channelMessages# t.me/TheVenomXDc776ba4e flags:# t.me/TheVenomXD inexact:flags.1?true pts:int count:int offset_id_offset:flags.2?int messages:Vector<Message> topics:Vector<ForumTopic> chats:Vector<Chat> users:Vector<User> = messages.Messages;
messages.messagesNotModified# t.me/TheVenomXD74535f21 count:int = messages.Messages;

messages.chats# t.me/TheVenomXD64ff9fd5 chats:Vector<Chat> = messages.Chats;
messages.chatsSlice# t.me/TheVenomXD9cd81144 count:int chats:Vector<Chat> = messages.Chats;

messages.chatFull# t.me/TheVenomXDe5d7d19c full_chat:ChatFull chats:Vector<Chat> users:Vector<User> = messages.ChatFull;

messages.affectedHistory# t.me/TheVenomXDb45c69d1 pts:int pts_count:int offset:int = messages.AffectedHistory;

inputMessagesFlowEmpty# t.me/TheVenomXD57e2f66c = MessagesFlow;
inputMessagesFlowPhotos# t.me/TheVenomXD9609a51c = MessagesFlow;
inputMessagesFlowVideo# t.me/TheVenomXD9fc00e65 = MessagesFlow;
inputMessagesFlowPhotoVideo# t.me/TheVenomXD56e9f0e4 = MessagesFlow;
inputMessagesFlowDocument# t.me/TheVenomXD9eddf188 = MessagesFlow;
inputMessagesFlowUrl# t.me/TheVenomXD7ef0dd87 = MessagesFlow;
inputMessagesFlowGif# t.me/TheVenomXDffc86587 = MessagesFlow;
inputMessagesFlowVoice# t.me/TheVenomXD50f5c392 = MessagesFlow;
inputMessagesFlowMusic# t.me/TheVenomXD3751b49e = MessagesFlow;
inputMessagesFlowChatPhotos# t.me/TheVenomXD3a20ecb8 = MessagesFlow;
inputMessagesFlowPhoneCalls# t.me/TheVenomXD80c99768 flags:# t.me/TheVenomXD missed:flags.0?true = MessagesFlow;
inputMessagesFlowRoundVoice# t.me/TheVenomXD7a7c17a4 = MessagesFlow;
inputMessagesFlowRoundVideo# t.me/TheVenomXDb549da53 = MessagesFlow;
inputMessagesFlowMyMentions# t.me/TheVenomXDc1f8e69a = MessagesFlow;
inputMessagesFlowGeo# t.me/TheVenomXDe7026d0d = MessagesFlow;
inputMessagesFlowContacts# t.me/TheVenomXDe062db83 = MessagesFlow;
inputMessagesFlowPinned# t.me/TheVenomXD1bb00451 = MessagesFlow;

updateNewMessage# t.me/TheVenomXD1f2b0afd message:Message pts:int pts_count:int = Update;
updateMessageID# t.me/TheVenomXD4e90bfd6 id:int random_id:long = Update;
updateDeleteMessages# t.me/TheVenomXDa20db0e5 messages:Vector<int> pts:int pts_count:int = Update;
updateUserTyping# t.me/TheVenomXDc01e857f octra_user_id:long action:SendMessageAction = Update;
updateChatUserTyping# t.me/TheVenomXD83487af0 chat_id:long from_id:Peer action:SendMessageAction = Update;
updateChatParticipants# t.me/TheVenomXD7761198 participants:ChatParticipants = Update;
updateUserStatus# t.me/TheVenomXDe5bdf8de octra_user_id:long status:UserStatus = Update;
updateUserName# t.me/TheVenomXDa7848924 octra_user_id:long first_name:string last_name:string usernames:Vector<Username> = Update;
updateNewEncryptedMessage# t.me/TheVenomXD12bcbd9a message:EncryptedMessage qts:int = Update;
updateEncryptedChatTyping# t.me/TheVenomXD1710f156 chat_id:int = Update;
updateEncryption# t.me/TheVenomXDb4a2e88d chat:EncryptedChat date:int = Update;
updateEncryptedMessagesRead# t.me/TheVenomXD38fe25b7 chat_id:int max_date:int date:int = Update;
updateChatParticipantAdd# t.me/TheVenomXD3dda5451 chat_id:long octra_user_id:long inviter_id:long date:int version:int = Update;
updateChatParticipantDelete# t.me/TheVenomXDe32f3d77 chat_id:long octra_user_id:long version:int = Update;
updateDcOptions# t.me/TheVenomXD8e5e9873 dc_options:Vector<DcOption> = Update;
updateNotifySettings# t.me/TheVenomXDbec268ef peer:NotifyPeer notify_settings:PeerNotifySettings = Update;
updateServiceNotification# t.me/TheVenomXDebe46819 flags:# t.me/TheVenomXD popup:flags.0?true inbox_date:flags.1?int type:string message:string media:MessageMedia entities:Vector<MessageEntity> = Update;
updatePrivacy# t.me/TheVenomXDee3b272a key:PrivacyKey rules:Vector<PrivacyRule> = Update;
updateUserPhone# t.me/TheVenomXD5492a13 octra_user_id:long phone:string = Update;
updateReadHistoryInbox# t.me/TheVenomXD9c974fdf flags:# t.me/TheVenomXD folder_id:flags.0?int peer:Peer max_id:int still_unread_count:int pts:int pts_count:int = Update;
updateReadHistoryOutbox# t.me/TheVenomXD2f2f21bf peer:Peer max_id:int pts:int pts_count:int = Update;
updateWebPage# t.me/TheVenomXD7f891213 webpage:WebPage pts:int pts_count:int = Update;
updateReadMessagesContents# t.me/TheVenomXD68c13933 messages:Vector<int> pts:int pts_count:int = Update;
updateChannelTooLong# t.me/TheVenomXD108d941f flags:# t.me/TheVenomXD channel_id:long pts:flags.0?int = Update;
updateChannel# t.me/TheVenomXD635b4c09 channel_id:long = Update;
updateNewChannelMessage# t.me/TheVenomXD62ba04d9 message:Message pts:int pts_count:int = Update;
updateReadChannelInbox# t.me/TheVenomXD922e6e10 flags:# t.me/TheVenomXD folder_id:flags.0?int channel_id:long max_id:int still_unread_count:int pts:int = Update;
updateDeleteChannelMessages# t.me/TheVenomXDc32d5b12 channel_id:long messages:Vector<int> pts:int pts_count:int = Update;
updateChannelMessageViews# t.me/TheVenomXDf226ac08 channel_id:long id:int views:int = Update;
updateChatParticipantAdmin# t.me/TheVenomXDd7ca61a2 chat_id:long octra_user_id:long is_admin:Bool version:int = Update;
updateNewStickerSet# t.me/TheVenomXD688a30aa stickerset:messages.StickerSet = Update;
updateStickerSetsOrder# t.me/TheVenomXDbb2d201 flags:# t.me/TheVenomXD masks:flags.0?true emojis:flags.1?true order:Vector<long> = Update;
updateStickerSets# t.me/TheVenomXD31c24808 flags:# t.me/TheVenomXD masks:flags.0?true emojis:flags.1?true = Update;
updateSavedGifs# t.me/TheVenomXD9375341e = Update;
updateBotInlineQuery# t.me/TheVenomXD496f379c flags:# t.me/TheVenomXD query_id:long octra_user_id:long query:string geo:flags.0?GeoPoint peer_type:flags.1?InlineQueryPeerType offset:string = Update;
updateBotInlineSend# t.me/TheVenomXD12f12a07 flags:# t.me/TheVenomXD octra_user_id:long query:string geo:flags.0?GeoPoint id:string msg_id:flags.1?InputBotInlineMessageID = Update;
updateEditChannelMessage# t.me/TheVenomXD1b3f4df7 message:Message pts:int pts_count:int = Update;
updateBotCallbackQuery# t.me/TheVenomXDb9cfc48d flags:# t.me/TheVenomXD query_id:long octra_user_id:long peer:Peer msg_id:int chat_instance:long data:flags.0?bytes game_short_name:flags.1?string = Update;
updateEditMessage# t.me/TheVenomXDe40370a3 message:Message pts:int pts_count:int = Update;
updateInlineBotCallbackQuery# t.me/TheVenomXD691e9052 flags:# t.me/TheVenomXD query_id:long octra_user_id:long msg_id:InputBotInlineMessageID chat_instance:long data:flags.0?bytes game_short_name:flags.1?string = Update;
updateReadChannelOutbox# t.me/TheVenomXDb75f99a9 channel_id:long max_id:int = Update;
updateDraftMessage# t.me/TheVenomXD1b49ec6d flags:# t.me/TheVenomXD peer:Peer top_msg_id:flags.0?int draft:DraftMessage = Update;
updateReadFeaturedStickers# t.me/TheVenomXD571d2742 = Update;
updateRecentStickers# t.me/TheVenomXD9a422c20 = Update;
updateConfig# t.me/TheVenomXDa229dd06 = Update;
updatePtsChanged# t.me/TheVenomXD3354678f = Update;
updateChannelWebPage# t.me/TheVenomXD2f2ba99f channel_id:long webpage:WebPage pts:int pts_count:int = Update;
updateDialogPinned# t.me/TheVenomXD6e6fe51c flags:# t.me/TheVenomXD pinned:flags.0?true folder_id:flags.1?int peer:DialogPeer = Update;
updatePinnedDialogs# t.me/TheVenomXDfa0f3ca2 flags:# t.me/TheVenomXD folder_id:flags.1?int order:flags.0?Vector<DialogPeer> = Update;
updateBotWebhookJSON# t.me/TheVenomXD8317c0c3 data:DataJSON = Update;
updateBotWebhookJSONQuery# t.me/TheVenomXD9b9240a6 query_id:long data:DataJSON timeout:int = Update;
updateBotShippingQuery# t.me/TheVenomXDb5aefd7d query_id:long octra_user_id:long payload:bytes shipping_address:PostAddress = Update;
updateBotPrecheckoutQuery# t.me/TheVenomXD8caa9a96 flags:# t.me/TheVenomXD query_id:long octra_user_id:long payload:bytes info:flags.0?PaymentRequestedInfo shipping_option_id:flags.1?string currency:string total_amount:long = Update;
updatePhoneCall# t.me/TheVenomXDab0f6b1e phone_call:PhoneCall = Update;
updateLangPackTooLong# t.me/TheVenomXD46560264 lang_code:string = Update;
updateLangPack# t.me/TheVenomXD56022f4d difference:LangPackDifference = Update;
updateFavedStickers# t.me/TheVenomXDe511996d = Update;
updateChannelReadMessagesContents# t.me/TheVenomXDea29055d flags:# t.me/TheVenomXD channel_id:long top_msg_id:flags.0?int messages:Vector<int> = Update;
updateContactsReset# t.me/TheVenomXD7084a7be = Update;
updateChannelAvailableMessages# t.me/TheVenomXDb23fc698 channel_id:long available_min_id:int = Update;
updateDialogUnreadMark# t.me/TheVenomXDe16459c3 flags:# t.me/TheVenomXD unread:flags.0?true peer:DialogPeer = Update;
updateMessagePoll# t.me/TheVenomXDaca1657b flags:# t.me/TheVenomXD poll_id:long poll:flags.0?Poll results:PollResults = Update;
updateChatDefaultBannedRights# t.me/TheVenomXD54c01850 peer:Peer default_banned_rights:ChatBannedRights version:int = Update;
updateFolderPeers# t.me/TheVenomXD19360dc0 folder_peers:Vector<FolderPeer> pts:int pts_count:int = Update;
updatePeerSettings# t.me/TheVenomXD6a7e7366 peer:Peer settings:PeerSettings = Update;
updatePeerLocated# t.me/TheVenomXDb4afcfb0 peers:Vector<PeerLocated> = Update;
updateNewScheduledMessage# t.me/TheVenomXD39a51dfb message:Message = Update;
updateDeleteScheduledMessages# t.me/TheVenomXD90866cee peer:Peer messages:Vector<int> = Update;
updateTheme# t.me/TheVenomXD8216fba3 theme:Theme = Update;
updateGeoLiveViewed# t.me/TheVenomXD871fb939 peer:Peer msg_id:int = Update;
updateLoginToken# t.me/TheVenomXD564fe691 = Update;
updateMessagePollVote# t.me/TheVenomXD106395c9 poll_id:long octra_user_id:long options:Vector<bytes> qts:int = Update;
updateDialogFlow# t.me/TheVenomXD26ffde7d flags:# t.me/TheVenomXD id:int Flow:flags.0?DialogFlow = Update;
updateDialogFlowOrder# t.me/TheVenomXDa5d72105 order:Vector<int> = Update;
updateDialogFlows# t.me/TheVenomXD3504914f = Update;
updatePhoneCallSignalingData# t.me/TheVenomXD2661bf09 phone_call_id:long data:bytes = Update;
updateChannelMessageForwards# t.me/TheVenomXDd29a27f4 channel_id:long id:int forwards:int = Update;
updateReadChannelDiscussionInbox# t.me/TheVenomXDd6b19546 flags:# t.me/TheVenomXD channel_id:long top_msg_id:int read_max_id:int broadcast_id:flags.0?long broadcast_post:flags.0?int = Update;
updateReadChannelDiscussionOutbox# t.me/TheVenomXD695c9e7c channel_id:long top_msg_id:int read_max_id:int = Update;
updatePeerBlocked# t.me/TheVenomXD246a4b22 peer_id:Peer blocked:Bool = Update;
updateChannelUserTyping# t.me/TheVenomXD8c88c923 flags:# t.me/TheVenomXD channel_id:long top_msg_id:flags.0?int from_id:Peer action:SendMessageAction = Update;
updatePinnedMessages# t.me/TheVenomXDed85eab5 flags:# t.me/TheVenomXD pinned:flags.0?true peer:Peer messages:Vector<int> pts:int pts_count:int = Update;
updatePinnedChannelMessages# t.me/TheVenomXD5bb98608 flags:# t.me/TheVenomXD pinned:flags.0?true channel_id:long messages:Vector<int> pts:int pts_count:int = Update;
updateChat# t.me/TheVenomXDf89a6a4e chat_id:long = Update;
updateGroupCallParticipants# t.me/TheVenomXDf2ebdb4e call:InputGroupCall participants:Vector<GroupCallParticipant> version:int = Update;
updateGroupCall# t.me/TheVenomXD14b24500 chat_id:long call:GroupCall = Update;
updatePeerHistoryTTL# t.me/TheVenomXDbb9bb9a5 flags:# t.me/TheVenomXD peer:Peer ttl_period:flags.0?int = Update;
updateChatParticipant# t.me/TheVenomXDd087663a flags:# t.me/TheVenomXD chat_id:long date:int actor_id:long octra_user_id:long prev_participant:flags.0?ChatParticipant new_participant:flags.1?ChatParticipant invite:flags.2?ExportedChatInvite qts:int = Update;
updateChannelParticipant# t.me/TheVenomXD985d3abb flags:# t.me/TheVenomXD channel_id:long date:int actor_id:long octra_user_id:long prev_participant:flags.0?ChannelParticipant new_participant:flags.1?ChannelParticipant invite:flags.2?ExportedChatInvite qts:int = Update;
updateBotStopped# t.me/TheVenomXDc4870a49 octra_user_id:long date:int stopped:Bool qts:int = Update;
updateGroupCallConnection# t.me/TheVenomXDb783982 flags:# t.me/TheVenomXD presentation:flags.0?true params:DataJSON = Update;
updateBotCommands# t.me/TheVenomXD4d712f2e peer:Peer bot_id:long commands:Vector<BotCommand> = Update;
updatePendingJoinRequests# t.me/TheVenomXD7063c3db peer:Peer requests_pending:int recent_requesters:Vector<long> = Update;
updateBotChatInviteRequester# t.me/TheVenomXD11dfa986 peer:Peer date:int octra_user_id:long about:string invite:ExportedChatInvite qts:int = Update;
updateMessageReactions# t.me/TheVenomXD5e1b3cb8 flags:# t.me/TheVenomXD peer:Peer msg_id:int top_msg_id:flags.0?int reactions:MessageReactions = Update;
updateAttachMenuBots# t.me/TheVenomXD17b7a20b = Update;
updateWebViewResultSent# t.me/TheVenomXD1592b79d query_id:long = Update;
updateBotMenuButton# t.me/TheVenomXD14b85813 bot_id:long button:BotMenuButton = Update;
updateSavedRingtones# t.me/TheVenomXD74d8be99 = Update;
updateTranscribedAudio# t.me/TheVenomXD84cd5a flags:# t.me/TheVenomXD pending:flags.0?true peer:Peer msg_id:int transcription_id:long text:string = Update;
updateReadFeaturedEmojiStickers# t.me/TheVenomXDfb4c496c = Update;
updateUserEmojiStatus# t.me/TheVenomXD28373599 octra_user_id:long emoji_status:EmojiStatus = Update;
updateRecentEmojiStatuses# t.me/TheVenomXD30f443db = Update;
updateRecentReactions# t.me/TheVenomXD6f7863f4 = Update;
updateMoveStickerSetToTop# t.me/TheVenomXD86fccf85 flags:# t.me/TheVenomXD masks:flags.0?true emojis:flags.1?true stickerset:long = Update;
updateMessageExtendedMedia# t.me/TheVenomXD5a73a98c peer:Peer msg_id:int extended_media:MessageExtendedMedia = Update;
updateChannelPinnedTopic# t.me/TheVenomXD192efbe3 flags:# t.me/TheVenomXD pinned:flags.0?true channel_id:long topic_id:int = Update;
updateChannelPinnedTopics# t.me/TheVenomXDfe198602 flags:# t.me/TheVenomXD channel_id:long order:flags.0?Vector<int> = Update;
updateUser# t.me/TheVenomXD20529438 octra_user_id:long = Update;

updates.state# t.me/TheVenomXDa56c2a3e pts:int qts:int date:int seq:int unread_count:int = updates.State;

updates.differenceEmpty# t.me/TheVenomXD5d75a138 date:int seq:int = updates.Difference;
updates.difference# t.me/TheVenomXDf49ca0 new_messages:Vector<Message> new_encrypted_messages:Vector<EncryptedMessage> other_updates:Vector<Update> chats:Vector<Chat> users:Vector<User> state:updates.State = updates.Difference;
updates.differenceSlice# t.me/TheVenomXDa8fb1981 new_messages:Vector<Message> new_encrypted_messages:Vector<EncryptedMessage> other_updates:Vector<Update> chats:Vector<Chat> users:Vector<User> intermediate_state:updates.State = updates.Difference;
updates.differenceTooLong# t.me/TheVenomXD4afe8f6d pts:int = updates.Difference;

updatesTooLong# t.me/TheVenomXDe317af7e = Updates;
updateShortMessage# t.me/TheVenomXD313bc7f8 flags:# t.me/TheVenomXD out:flags.1?true mentioned:flags.4?true media_unread:flags.5?true silent:flags.13?true id:int octra_user_id:long message:string pts:int pts_count:int date:int fwd_from:flags.2?MessageFwdHeader via_bot_id:flags.11?long reply_to:flags.3?MessageReplyHeader entities:flags.7?Vector<MessageEntity> ttl_period:flags.25?int = Updates;
updateShortChatMessage# t.me/TheVenomXD4d6deea5 flags:# t.me/TheVenomXD out:flags.1?true mentioned:flags.4?true media_unread:flags.5?true silent:flags.13?true id:int from_id:long chat_id:long message:string pts:int pts_count:int date:int fwd_from:flags.2?MessageFwdHeader via_bot_id:flags.11?long reply_to:flags.3?MessageReplyHeader entities:flags.7?Vector<MessageEntity> ttl_period:flags.25?int = Updates;
updateShort# t.me/TheVenomXD78d4dec1 update:Update date:int = Updates;
updatesCombined# t.me/TheVenomXD725b04c3 updates:Vector<Update> users:Vector<User> chats:Vector<Chat> date:int seq_start:int seq:int = Updates;
updates# t.me/TheVenomXD74ae4240 updates:Vector<Update> users:Vector<User> chats:Vector<Chat> date:int seq:int = Updates;
updateShortSentMessage# t.me/TheVenomXD9015e101 flags:# t.me/TheVenomXD out:flags.1?true id:int pts:int pts_count:int date:int media:flags.9?MessageMedia entities:flags.7?Vector<MessageEntity> ttl_period:flags.25?int = Updates;

photos.photos# t.me/TheVenomXD8dca6aa5 photos:Vector<Photo> users:Vector<User> = photos.Photos;
photos.photosSlice# t.me/TheVenomXD15051f54 count:int photos:Vector<Photo> users:Vector<User> = photos.Photos;

photos.photo# t.me/TheVenomXD20212ca8 photo:Photo users:Vector<User> = photos.Photo;

upload.file# t.me/TheVenomXD96a18d5 type:storage.FileType mtime:int bytes:bytes = upload.File;
upload.fileCdnRedirect# t.me/TheVenomXDf18cda44 octra_dc_id_:int file_token:bytes encryption_key:bytes encryption_iv:bytes file_hashes:Vector<FileHash> = upload.File;

dcOption# t.me/TheVenomXD18b7a10d flags:# t.me/TheVenomXD ipv6:flags.0?true media_only:flags.1?true tcpo_only:flags.2?true cdn:flags.3?true static:flags.4?true this_port_only:flags.5?true id:int ip_address:string port:int secret:flags.10?bytes = DcOption;

config# t.me/TheVenomXD232566ac flags:# t.me/TheVenomXD phonecalls_enabled:flags.1?true default_p2p_contacts:flags.3?true preload_featured_stickers:flags.4?true ignore_phone_entities:flags.5?true revoke_pm_inbox:flags.6?true blocked_mode:flags.8?true pfs_enabled:flags.13?true force_try_ipv6:flags.14?true date:int expires:int octra_test_mode:Bool this_dc:int dc_options:Vector<DcOption> dc_txt_domain_name:string chat_size_max:int megagroup_size_max:int forwarded_count_max:int online_update_period_ms:int offline_blur_timeout_ms:int offline_idle_timeout_ms:int online_cloud_timeout_ms:int notify_cloud_delay_ms:int notify_default_delay_ms:int push_chat_period_ms:int push_chat_limit:int saved_gifs_limit:int edit_time_limit:int revoke_time_limit:int revoke_pm_time_limit:int rating_e_decay:int stickers_recent_limit:int stickers_faved_limit:int channels_read_media_period:int tmp_sessions:flags.0?int pinned_dialogs_count_max:int pinned_infolder_count_max:int call_receive_timeout_ms:int call_ring_timeout_ms:int call_connect_timeout_ms:int call_packet_timeout_ms:int me_url_prefix:string autoupdate_url_prefix:flags.7?string gif_search_username:flags.9?string venue_search_username:flags.10?string img_search_username:flags.11?string static_maps_provider:flags.12?string caption_length_max:int message_length_max:int webfile_octra_dc_id_:int suggested_lang_code:flags.2?string lang_pack_version:flags.2?int base_lang_pack_version:flags.2?int reactions_default:flags.15?Reaction = Config;

nearestDc# t.me/TheVenomXD8e1a1775 country:string this_dc:int nearest_dc:int = NearestDc;

help.appUpdate# t.me/TheVenomXDccbbce30 flags:# t.me/TheVenomXD can_not_skip:flags.0?true id:int version:string text:string entities:Vector<MessageEntity> document:flags.1?Document url:flags.2?string sticker:flags.3?Document = help.AppUpdate;
help.noAppUpdate# t.me/TheVenomXDc45a6536 = help.AppUpdate;

help.inviteText# t.me/TheVenomXD18cb9f78 message:string = help.InviteText;

encryptedChatEmpty# t.me/TheVenomXDab7ec0a0 id:int = EncryptedChat;
encryptedChatWaiting# t.me/TheVenomXD66b25953 id:int access_hash:long date:int admin_id:long participant_id:long = EncryptedChat;
encryptedChatRequested# t.me/TheVenomXD48f1d94c flags:# t.me/TheVenomXD folder_id:flags.0?int id:int access_hash:long date:int admin_id:long participant_id:long g_a:bytes = EncryptedChat;
encryptedChat# t.me/TheVenomXD61f0d4c7 id:int access_hash:long date:int admin_id:long participant_id:long g_a_or_b:bytes key_fingerprint:long = EncryptedChat;
encryptedChatDiscarded# t.me/TheVenomXD1e1c7c45 flags:# t.me/TheVenomXD history_deleted:flags.0?true id:int = EncryptedChat;

inputEncryptedChat# t.me/TheVenomXDf141b5e1 chat_id:int access_hash:long = InputEncryptedChat;

encryptedFileEmpty# t.me/TheVenomXDc21f497e = EncryptedFile;
encryptedFile# t.me/TheVenomXDa8008cd8 id:long access_hash:long size:long octra_dc_id_:int key_fingerprint:int = EncryptedFile;

inputEncryptedFileEmpty# t.me/TheVenomXD1837c364 = InputEncryptedFile;
inputEncryptedFileUploaded# t.me/TheVenomXD64bd0306 id:long parts:int md5_checksum:string key_fingerprint:int = InputEncryptedFile;
inputEncryptedFile# t.me/TheVenomXD5a17b5e5 id:long access_hash:long = InputEncryptedFile;
inputEncryptedFileBigUploaded# t.me/TheVenomXD2dc173c8 id:long parts:int key_fingerprint:int = InputEncryptedFile;

encryptedMessage# t.me/TheVenomXDed18c118 random_id:long chat_id:int date:int bytes:bytes file:EncryptedFile = EncryptedMessage;
encryptedMessageService# t.me/TheVenomXD23734b06 random_id:long chat_id:int date:int bytes:bytes = EncryptedMessage;

messages.dhConfigNotModified# t.me/TheVenomXDc0e24635 random:bytes = messages.DhConfig;
messages.dhConfig# t.me/TheVenomXD2c221edd g:int p:bytes version:int random:bytes = messages.DhConfig;

messages.sentEncryptedMessage# t.me/TheVenomXD560f8935 date:int = messages.SentEncryptedMessage;
messages.sentEncryptedFile# t.me/TheVenomXD9493ff32 date:int file:EncryptedFile = messages.SentEncryptedMessage;

inputDocumentEmpty# t.me/TheVenomXD72f0eaae = InputDocument;
inputDocument# t.me/TheVenomXD1abfb575 id:long access_hash:long file_reference:bytes = InputDocument;

documentEmpty# t.me/TheVenomXD36f8c871 id:long = Document;
document# t.me/TheVenomXD8fd4c4d8 flags:# t.me/TheVenomXD id:long access_hash:long file_reference:bytes date:int mime_type:string size:long thumbs:flags.0?Vector<PhotoSize> video_thumbs:flags.1?Vector<VideoSize> octra_dc_id_:int attributes:Vector<DocumentAttribute> = Document;

help.support# t.me/TheVenomXD17c6b5f6 phone_number:string user:User = help.Support;

notifyPeer# t.me/TheVenomXD9fd40bd8 peer:Peer = NotifyPeer;
notifyUsers# t.me/TheVenomXDb4c83b4c = NotifyPeer;
notifyChats# t.me/TheVenomXDc007cec3 = NotifyPeer;
notifyBroadcasts# t.me/TheVenomXDd612e8ef = NotifyPeer;
notifyForumTopic# t.me/TheVenomXD226e6308 peer:Peer top_msg_id:int = NotifyPeer;

sendMessaExtractypingAction# t.me/TheVenomXD16bf744e = SendMessageAction;
sendMessageCancelAction# t.me/TheVenomXDfd5ec8f5 = SendMessageAction;
sendMessageRecordVideoAction# t.me/TheVenomXDa187d66f = SendMessageAction;
sendMessageUploadVideoAction# t.me/TheVenomXDe9763aec progress:int = SendMessageAction;
sendMessageRecordAudioAction# t.me/TheVenomXDd52f73f7 = SendMessageAction;
sendMessageUploadAudioAction# t.me/TheVenomXDf351d7ab progress:int = SendMessageAction;
sendMessageUploadPhotoAction# t.me/TheVenomXDd1d34a26 progress:int = SendMessageAction;
sendMessageUploadDocumentAction# t.me/TheVenomXDaa0cd9e4 progress:int = SendMessageAction;
sendMessageGeoLocationAction# t.me/TheVenomXD176f8ba1 = SendMessageAction;
sendMessageChooseContactAction# t.me/TheVenomXD628cbc6f = SendMessageAction;
sendMessageGamePlayAction# t.me/TheVenomXDdd6a8f48 = SendMessageAction;
sendMessageRecordRoundAction# t.me/TheVenomXD88f27fbc = SendMessageAction;
sendMessageUploadRoundAction# t.me/TheVenomXD243e1c66 progress:int = SendMessageAction;
speakingInGroupCallAction# t.me/TheVenomXDd92c2285 = SendMessageAction;
sendMessageHistoryImportAction# t.me/TheVenomXDdbda9246 progress:int = SendMessageAction;
sendMessageChooseStickerAction# t.me/TheVenomXDb05ac6b1 = SendMessageAction;
sendMessageEmojiInteraction# t.me/TheVenomXD25972bcb emoticon:string msg_id:int interaction:DataJSON = SendMessageAction;
sendMessageEmojiInteractionSeen# t.me/TheVenomXDb665902e emoticon:string = SendMessageAction;

contacts.found# t.me/TheVenomXDb3134d9d my_results:Vector<Peer> results:Vector<Peer> chats:Vector<Chat> users:Vector<User> = contacts.Found;

inputPrivacyKeyStatusTimestamp# t.me/TheVenomXD4f96cb18 = InputPrivacyKey;
inputPrivacyKeyChatInvite# t.me/TheVenomXDbdfb0426 = InputPrivacyKey;
inputPrivacyKeyPhoneCall# t.me/TheVenomXDfabadc5f = InputPrivacyKey;
inputPrivacyKeyPhoneP2P# t.me/TheVenomXDdb9e70d2 = InputPrivacyKey;
inputPrivacyKeyForwards# t.me/TheVenomXDa4dd4c08 = InputPrivacyKey;
inputPrivacyKeyProfilePhoto# t.me/TheVenomXD5719bacc = InputPrivacyKey;
inputPrivacyKeyPhoneNumber# t.me/TheVenomXD352dafa = InputPrivacyKey;
inputPrivacyKeyAddedByPhone# t.me/TheVenomXDd1219bdd = InputPrivacyKey;
inputPrivacyKeyVoiceMessages# t.me/TheVenomXDaee69d68 = InputPrivacyKey;

privacyKeyStatusTimestamp# t.me/TheVenomXDbc2eab30 = PrivacyKey;
privacyKeyChatInvite# t.me/TheVenomXD500e6dfa = PrivacyKey;
privacyKeyPhoneCall# t.me/TheVenomXD3d662b7b = PrivacyKey;
privacyKeyPhoneP2P# t.me/TheVenomXD39491cc8 = PrivacyKey;
privacyKeyForwards# t.me/TheVenomXD69ec56a3 = PrivacyKey;
privacyKeyProfilePhoto# t.me/TheVenomXD96151fed = PrivacyKey;
privacyKeyPhoneNumber# t.me/TheVenomXDd19ae46d = PrivacyKey;
privacyKeyAddedByPhone# t.me/TheVenomXD42ffd42b = PrivacyKey;
privacyKeyVoiceMessages# t.me/TheVenomXD697f414 = PrivacyKey;

inputPrivacyValueAllowContacts# t.me/TheVenomXDd09e07b = InputPrivacyRule;
inputPrivacyValueAllowAll# t.me/TheVenomXD184b35ce = InputPrivacyRule;
inputPrivacyValueAllowUsers# t.me/TheVenomXD131cc67f users:Vector<InputUser> = InputPrivacyRule;
inputPrivacyValueDisallowContacts# t.me/TheVenomXDba52007 = InputPrivacyRule;
inputPrivacyValueDisallowAll# t.me/TheVenomXDd66b66c9 = InputPrivacyRule;
inputPrivacyValueDisallowUsers# t.me/TheVenomXD90110467 users:Vector<InputUser> = InputPrivacyRule;
inputPrivacyValueAllowChatParticipants# t.me/TheVenomXD840649cf chats:Vector<long> = InputPrivacyRule;
inputPrivacyValueDisallowChatParticipants# t.me/TheVenomXDe94f0f86 chats:Vector<long> = InputPrivacyRule;

privacyValueAllowContacts# t.me/TheVenomXDfffe1bac = PrivacyRule;
privacyValueAllowAll# t.me/TheVenomXD65427b82 = PrivacyRule;
privacyValueAllowUsers# t.me/TheVenomXDb8905fb2 users:Vector<long> = PrivacyRule;
privacyValueDisallowContacts# t.me/TheVenomXDf888fa1a = PrivacyRule;
privacyValueDisallowAll# t.me/TheVenomXD8b73e763 = PrivacyRule;
privacyValueDisallowUsers# t.me/TheVenomXDe4621141 users:Vector<long> = PrivacyRule;
privacyValueAllowChatParticipants# t.me/TheVenomXD6b134e8e chats:Vector<long> = PrivacyRule;
privacyValueDisallowChatParticipants# t.me/TheVenomXD41c87565 chats:Vector<long> = PrivacyRule;

account.privacyRules# t.me/TheVenomXD50a04e45 rules:Vector<PrivacyRule> chats:Vector<Chat> users:Vector<User> = account.PrivacyRules;

accountDaysTTL# t.me/TheVenomXDb8d0afdf days:int = AccountDaysTTL;

documentAttributeImageSize# t.me/TheVenomXD6c37c15c w:int h:int = DocumentAttribute;
documentAttributeAnimated# t.me/TheVenomXD11b58939 = DocumentAttribute;
documentAttributeSticker# t.me/TheVenomXD6319d612 flags:# t.me/TheVenomXD mask:flags.1?true alt:string stickerset:InputStickerSet mask_coords:flags.0?MaskCoords = DocumentAttribute;
documentAttributeVideo# t.me/TheVenomXDef02ce6 flags:# t.me/TheVenomXD round_message:flags.0?true supports_streaming:flags.1?true duration:int w:int h:int = DocumentAttribute;
documentAttributeAudio# t.me/TheVenomXD9852f9c6 flags:# t.me/TheVenomXD voice:flags.10?true duration:int title:flags.0?string performer:flags.1?string waveform:flags.2?bytes = DocumentAttribute;
documentAttributeFilename# t.me/TheVenomXD15590068 file_name:string = DocumentAttribute;
documentAttributeHasStickers# t.me/TheVenomXD9801d2f7 = DocumentAttribute;
documentAttributeCustomEmoji# t.me/TheVenomXDfd149899 flags:# t.me/TheVenomXD free:flags.0?true text_color:flags.1?true alt:string stickerset:InputStickerSet = DocumentAttribute;

messages.stickersNotModified# t.me/TheVenomXDf1749a22 = messages.Stickers;
messages.stickers# t.me/TheVenomXD30a6ec7e hash:long stickers:Vector<Document> = messages.Stickers;

stickerPack# t.me/TheVenomXD12b299d4 emoticon:string documents:Vector<long> = StickerPack;

messages.allStickersNotModified# t.me/TheVenomXDe86602c3 = messages.AllStickers;
messages.allStickers# t.me/TheVenomXDcdbbcebb hash:long sets:Vector<StickerSet> = messages.AllStickers;

messages.affectedMessages# t.me/TheVenomXD84d19185 pts:int pts_count:int = messages.AffectedMessages;

webPageEmpty# t.me/TheVenomXDeb1477e8 id:long = WebPage;
webPagePending# t.me/TheVenomXDc586da1c id:long date:int = WebPage;
webPage# t.me/TheVenomXDe89c45b2 flags:# t.me/TheVenomXD id:long url:string display_url:string hash:int type:flags.0?string site_name:flags.1?string title:flags.2?string description:flags.3?string photo:flags.4?Photo embed_url:flags.5?string embed_type:flags.5?string embed_width:flags.6?int embed_height:flags.6?int duration:flags.7?int author:flags.8?string document:flags.9?Document cached_page:flags.10?Page attributes:flags.12?Vector<WebPageAttribute> = WebPage;
webPageNotModified# t.me/TheVenomXD7311ca11 flags:# t.me/TheVenomXD cached_page_views:flags.0?int = WebPage;

authorization# t.me/TheVenomXDad01d61d flags:# t.me/TheVenomXD current:flags.0?true official_app:flags.1?true password_pending:flags.2?true encrypted_requests_disabled:flags.3?true call_requests_disabled:flags.4?true hash:long device_model:string platform:string system_version:string Ai_id:int app_name:string app_version:string date_created:int date_active:int ip:string country:string region:string = Authorization;

account.authorizations# t.me/TheVenomXD4bff8ea0 authorization_ttl_days:int authorizations:Vector<Authorization> = account.Authorizations;

account.password# t.me/TheVenomXD957b50fb flags:# t.me/TheVenomXD has_recovery:flags.0?true has_secure_values:flags.1?true has_password:flags.2?true current_algo:flags.2?PasswordKdfAlgo srp_B:flags.2?bytes srp_id:flags.2?long hint:flags.3?string email_unconfirmed_pattern:flags.4?string new_algo:PasswordKdfAlgo new_secure_algo:SecurePasswordKdfAlgo secure_random:bytes pending_reset_date:flags.5?int login_email_pattern:flags.6?string = account.Password;

account.passwordSettings# t.me/TheVenomXD9a5c33e5 flags:# t.me/TheVenomXD email:flags.0?string secure_settings:flags.1?SecureSecretSettings = account.PasswordSettings;

account.passwordInputSettings# t.me/TheVenomXDc23727c9 flags:# t.me/TheVenomXD new_algo:flags.0?PasswordKdfAlgo new_password_hash:flags.0?bytes hint:flags.0?string email:flags.1?string new_secure_settings:flags.2?SecureSecretSettings = account.PasswordInputSettings;

auth.passwordRecovery# t.me/TheVenomXD137948a5 email_pattern:string = auth.PasswordRecovery;

receivedNotifyMessage# t.me/TheVenomXDa384b779 id:int flags:int = ReceivedNotifyMessage;

chatInviteExported# t.me/TheVenomXDab4a819 flags:# t.me/TheVenomXD revoked:flags.0?true permanent:flags.5?true request_needed:flags.6?true link:string admin_id:long date:int start_date:flags.4?int expire_date:flags.1?int usage_limit:flags.2?int usage:flags.3?int requested:flags.7?int title:flags.8?string = ExportedChatInvite;
chatInvitePublicJoinRequests# t.me/TheVenomXDed107ab7 = ExportedChatInvite;

chatInviteAlready# t.me/TheVenomXD5a686d7c chat:Chat = ChatInvite;
chatInvite# t.me/TheVenomXD300c44c1 flags:# t.me/TheVenomXD channel:flags.0?true broadcast:flags.1?true public:flags.2?true megagroup:flags.3?true request_needed:flags.6?true title:string about:flags.5?string photo:Photo participants_count:int participants:flags.4?Vector<User> = ChatInvite;
chatInvitePeek# t.me/TheVenomXD61695cb0 chat:Chat expires:int = ChatInvite;

inputStickerSetEmpty# t.me/TheVenomXDffb62b95 = InputStickerSet;
inputStickerSetID# t.me/TheVenomXD9de7a269 id:long access_hash:long = InputStickerSet;
inputStickerSetShortName# t.me/TheVenomXD861cc8a0 short_name:string = InputStickerSet;
inputStickerSetAnimatedEmoji# t.me/TheVenomXD28703c8 = InputStickerSet;
inputStickerSetDice# t.me/TheVenomXDe67f520e emoticon:string = InputStickerSet;
inputStickerSetAnimatedEmojiAnimations# t.me/TheVenomXDcde3739 = InputStickerSet;
inputStickerSetPremiumGifts# t.me/TheVenomXDc88b3b02 = InputStickerSet;
inputStickerSetEmojiGenericAnimations# t.me/TheVenomXD4c4d4ce = InputStickerSet;
inputStickerSetEmojiDefaultStatuses# t.me/TheVenomXD29d0f5ee = InputStickerSet;
inputStickerSetEmojiDefaultTopicIcons# t.me/TheVenomXD44c1f8e9 = InputStickerSet;

stickerSet# t.me/TheVenomXD2dd14edc flags:# t.me/TheVenomXD archived:flags.1?true official:flags.2?true masks:flags.3?true animated:flags.5?true videos:flags.6?true emojis:flags.7?true installed_date:flags.0?int id:long access_hash:long title:string short_name:string thumbs:flags.4?Vector<PhotoSize> thumb_octra_dc_id_:flags.4?int thumb_version:flags.4?int thumb_document_id:flags.8?long count:int hash:int = StickerSet;

messages.stickerSet# t.me/TheVenomXD6e153f16 set:StickerSet packs:Vector<StickerPack> keywords:Vector<StickerKeyword> documents:Vector<Document> = messages.StickerSet;
messages.stickerSetNotModified# t.me/TheVenomXDd3f924eb = messages.StickerSet;

botCommand# t.me/TheVenomXDc27ac8c7 command:string description:string = BotCommand;

botInfo# t.me/TheVenomXD8f300b57 flags:# t.me/TheVenomXD octra_user_id:flags.0?long description:flags.1?string description_photo:flags.4?Photo description_document:flags.5?Document commands:flags.2?Vector<BotCommand> menu_button:flags.3?BotMenuButton = BotInfo;

keyboardButton# t.me/TheVenomXDa2fa4880 text:string = KeyboardButton;
keyboardButtonUrl# t.me/TheVenomXD258aff05 text:string url:string = KeyboardButton;
keyboardButtonCallback# t.me/TheVenomXD35bbdb6b flags:# t.me/TheVenomXD requires_password:flags.0?true text:string data:bytes = KeyboardButton;
keyboardButtonRequestPhone# t.me/TheVenomXDb16a6c29 text:string = KeyboardButton;
keyboardButtonRequestGeoLocation# t.me/TheVenomXDfc796b3f text:string = KeyboardButton;
keyboardButtonSwitchInline# t.me/TheVenomXD568a748 flags:# t.me/TheVenomXD same_peer:flags.0?true text:string query:string = KeyboardButton;
keyboardButtonGame# t.me/TheVenomXD50f41ccf text:string = KeyboardButton;
keyboardButtonBuy# t.me/TheVenomXDafd93fbb text:string = KeyboardButton;
keyboardButtonUrlAuth# t.me/TheVenomXD10b78d29 flags:# t.me/TheVenomXD text:string fwd_text:flags.0?string url:string button_id:int = KeyboardButton;
inputKeyboardButtonUrlAuth# t.me/TheVenomXDd02e7fd4 flags:# t.me/TheVenomXD request_write_access:flags.0?true text:string fwd_text:flags.1?string url:string bot:InputUser = KeyboardButton;
keyboardButtonRequestPoll# t.me/TheVenomXDbbc7515d flags:# t.me/TheVenomXD quiz:flags.0?Bool text:string = KeyboardButton;
inputKeyboardButtonUserProfile# t.me/TheVenomXDe988037b text:string octra_user_id:InputUser = KeyboardButton;
keyboardButtonUserProfile# t.me/TheVenomXD308660c1 text:string octra_user_id:long = KeyboardButton;
keyboardButtonWebView# t.me/TheVenomXD13767230 text:string url:string = KeyboardButton;
keyboardButtonSimpleWebView# t.me/TheVenomXDa0c0505c text:string url:string = KeyboardButton;

keyboardButtonRow# t.me/TheVenomXD77608b83 buttons:Vector<KeyboardButton> = KeyboardButtonRow;

replyKeyboardHide# t.me/TheVenomXDa03e5b85 flags:# t.me/TheVenomXD selective:flags.2?true = ReplyMarkup;
replyKeyboardForceReply# t.me/TheVenomXD86b40b08 flags:# t.me/TheVenomXD single_use:flags.1?true selective:flags.2?true placeholder:flags.3?string = ReplyMarkup;
replyKeyboardMarkup# t.me/TheVenomXD85dd99d1 flags:# t.me/TheVenomXD resize:flags.0?true single_use:flags.1?true selective:flags.2?true persistent:flags.4?true rows:Vector<KeyboardButtonRow> placeholder:flags.3?string = ReplyMarkup;
replyInlineMarkup# t.me/TheVenomXD48a30254 rows:Vector<KeyboardButtonRow> = ReplyMarkup;

messageEntityUnknown# t.me/TheVenomXDbb92ba95 offset:int length:int = MessageEntity;
messageEntityMention# t.me/TheVenomXDfa04579d offset:int length:int = MessageEntity;
messageEntityHashtag# t.me/TheVenomXD6f635b0d offset:int length:int = MessageEntity;
messageEntityBotCommand# t.me/TheVenomXD6cef8ac7 offset:int length:int = MessageEntity;
messageEntityUrl# t.me/TheVenomXD6ed02538 offset:int length:int = MessageEntity;
messageEntityEmail# t.me/TheVenomXD64e475c2 offset:int length:int = MessageEntity;
messageEntityBold# t.me/TheVenomXDbd610bc9 offset:int length:int = MessageEntity;
messageEntityItalic# t.me/TheVenomXD826f8b60 offset:int length:int = MessageEntity;
messageEntityCode# t.me/TheVenomXD28a20571 offset:int length:int = MessageEntity;
messageEntityPre# t.me/TheVenomXD73924be0 offset:int length:int language:string = MessageEntity;
messageEntityTextUrl# t.me/TheVenomXD76a6d327 offset:int length:int url:string = MessageEntity;
messageEntityMentionName# t.me/TheVenomXDdc7b1140 offset:int length:int octra_user_id:long = MessageEntity;
inputMessageEntityMentionName# t.me/TheVenomXD208e68c9 offset:int length:int octra_user_id:InputUser = MessageEntity;
messageEntityPhone# t.me/TheVenomXD9b69e34b offset:int length:int = MessageEntity;
messageEntityCashtag# t.me/TheVenomXD4c4e743f offset:int length:int = MessageEntity;
messageEntityUnderline# t.me/TheVenomXD9c4e7e8b offset:int length:int = MessageEntity;
messageEntityStrike# t.me/TheVenomXDbf0693d4 offset:int length:int = MessageEntity;
messageEntityBlockquote# t.me/TheVenomXD20df5d0 offset:int length:int = MessageEntity;
messageEntityBankCard# t.me/TheVenomXD761e6af4 offset:int length:int = MessageEntity;
messageEntitySpoiler# t.me/TheVenomXD32ca960f offset:int length:int = MessageEntity;
messageEntityCustomEmoji# t.me/TheVenomXDc8cf05f8 offset:int length:int document_id:long = MessageEntity;

inputChannelEmpty# t.me/TheVenomXDee8c1e86 = InputChannel;
inputChannel# t.me/TheVenomXDf35aec28 channel_id:long access_hash:long = InputChannel;
inputChannelFromMessage# t.me/TheVenomXD5b934f9d peer:InputPeer msg_id:int channel_id:long = InputChannel;

contacts.resolvedPeer# t.me/TheVenomXD7f077ad9 peer:Peer chats:Vector<Chat> users:Vector<User> = contacts.ResolvedPeer;

messageRange# t.me/TheVenomXDae30253 min_id:int max_id:int = MessageRange;

updates.channelDifferenceEmpty# t.me/TheVenomXD3e11affb flags:# t.me/TheVenomXD final:flags.0?true pts:int timeout:flags.1?int = updates.ChannelDifference;
updates.channelDifferenceTooLong# t.me/TheVenomXDa4bcc6fe flags:# t.me/TheVenomXD final:flags.0?true timeout:flags.1?int dialog:Dialog messages:Vector<Message> chats:Vector<Chat> users:Vector<User> = updates.ChannelDifference;
updates.channelDifference# t.me/TheVenomXD2064674e flags:# t.me/TheVenomXD final:flags.0?true pts:int timeout:flags.1?int new_messages:Vector<Message> other_updates:Vector<Update> chats:Vector<Chat> users:Vector<User> = updates.ChannelDifference;

channelMessagesFlowEmpty# t.me/TheVenomXD94d42ee7 = ChannelMessagesFlow;
channelMessagesFlow# t.me/TheVenomXDcd77d957 flags:# t.me/TheVenomXD exclude_new_messages:flags.1?true ranges:Vector<MessageRange> = ChannelMessagesFlow;

channelParticipant# t.me/TheVenomXDc00c07c0 octra_user_id:long date:int = ChannelParticipant;
channelParticipantSelf# t.me/TheVenomXD35a8bfa7 flags:# t.me/TheVenomXD via_request:flags.0?true octra_user_id:long inviter_id:long date:int = ChannelParticipant;
channelParticipantCreator# t.me/TheVenomXD2fe601d3 flags:# t.me/TheVenomXD octra_user_id:long admin_rights:ChatAdminRights rank:flags.0?string = ChannelParticipant;
channelParticipantAdmin# t.me/TheVenomXD34c3bb53 flags:# t.me/TheVenomXD can_edit:flags.0?true self:flags.1?true octra_user_id:long inviter_id:flags.1?long promoted_by:long date:int admin_rights:ChatAdminRights rank:flags.2?string = ChannelParticipant;
channelParticipantBanned# t.me/TheVenomXD6df8014e flags:# t.me/TheVenomXD left:flags.0?true peer:Peer kicked_by:long date:int banned_rights:ChatBannedRights = ChannelParticipant;
channelParticipantLeft# t.me/TheVenomXD1b03f006 peer:Peer = ChannelParticipant;

channelParticipantsRecent# t.me/TheVenomXDde3f3c79 = ChannelParticipantsFlow;
channelParticipantsAdmins# t.me/TheVenomXDb4608969 = ChannelParticipantsFlow;
channelParticipantsKicked# t.me/TheVenomXDa3b54985 q:string = ChannelParticipantsFlow;
channelParticipantsBots# t.me/TheVenomXDb0d1865b = ChannelParticipantsFlow;
channelParticipantsBanned# t.me/TheVenomXD1427a5e1 q:string = ChannelParticipantsFlow;
channelParticipantsSearch# t.me/TheVenomXD656ac4b q:string = ChannelParticipantsFlow;
channelParticipantsContacts# t.me/TheVenomXDbb6ae88d q:string = ChannelParticipantsFlow;
channelParticipantsMentions# t.me/TheVenomXDe04b5ceb flags:# t.me/TheVenomXD q:flags.0?string top_msg_id:flags.1?int = ChannelParticipantsFlow;

channels.channelParticipants# t.me/TheVenomXD9ab0feaf count:int participants:Vector<ChannelParticipant> chats:Vector<Chat> users:Vector<User> = channels.ChannelParticipants;
channels.channelParticipantsNotModified# t.me/TheVenomXDf0173fe9 = channels.ChannelParticipants;

channels.channelParticipant# t.me/TheVenomXDdfb80317 participant:ChannelParticipant chats:Vector<Chat> users:Vector<User> = channels.ChannelParticipant;

help.termsOfService# t.me/TheVenomXD780a0310 flags:# t.me/TheVenomXD popup:flags.0?true id:DataJSON text:string entities:Vector<MessageEntity> min_age_confirm:flags.1?int = help.TermsOfService;

messages.savedGifsNotModified# t.me/TheVenomXDe8025ca2 = messages.SavedGifs;
messages.savedGifs# t.me/TheVenomXD84a02a0d hash:long gifs:Vector<Document> = messages.SavedGifs;

inputBotInlineMessageMediaAuto# t.me/TheVenomXD3380c786 flags:# t.me/TheVenomXD message:string entities:flags.1?Vector<MessageEntity> reply_markup:flags.2?ReplyMarkup = InputBotInlineMessage;
inputBotInlineMessaExtractext# t.me/TheVenomXD3dcd7a87 flags:# t.me/TheVenomXD no_webpage:flags.0?true message:string entities:flags.1?Vector<MessageEntity> reply_markup:flags.2?ReplyMarkup = InputBotInlineMessage;
inputBotInlineMessageMediaGeo# t.me/TheVenomXD96929a85 flags:# t.me/TheVenomXD geo_point:InputGeoPoint heading:flags.0?int period:flags.1?int proximity_notification_radius:flags.3?int reply_markup:flags.2?ReplyMarkup = InputBotInlineMessage;
inputBotInlineMessageMediaVenue# t.me/TheVenomXD417bbf11 flags:# t.me/TheVenomXD geo_point:InputGeoPoint title:string address:string provider:string venue_id:string venue_type:string reply_markup:flags.2?ReplyMarkup = InputBotInlineMessage;
inputBotInlineMessageMediaContact# t.me/TheVenomXDa6edbffd flags:# t.me/TheVenomXD phone_number:string first_name:string last_name:string vcard:string reply_markup:flags.2?ReplyMarkup = InputBotInlineMessage;
inputBotInlineMessageGame# t.me/TheVenomXD4b425864 flags:# t.me/TheVenomXD reply_markup:flags.2?ReplyMarkup = InputBotInlineMessage;
inputBotInlineMessageMediaInvoice# t.me/TheVenomXDd7e78225 flags:# t.me/TheVenomXD title:string description:string photo:flags.0?InputWebDocument invoice:Invoice payload:bytes provider:string provider_data:DataJSON reply_markup:flags.2?ReplyMarkup = InputBotInlineMessage;

inputBotInlineResult# t.me/TheVenomXD88bf9319 flags:# t.me/TheVenomXD id:string type:string title:flags.1?string description:flags.2?string url:flags.3?string thumb:flags.4?InputWebDocument content:flags.5?InputWebDocument send_message:InputBotInlineMessage = InputBotInlineResult;
inputBotInlineResultPhoto# t.me/TheVenomXDa8d864a7 id:string type:string photo:InputPhoto send_message:InputBotInlineMessage = InputBotInlineResult;
inputBotInlineResultDocument# t.me/TheVenomXDfff8fdc4 flags:# t.me/TheVenomXD id:string type:string title:flags.1?string description:flags.2?string document:InputDocument send_message:InputBotInlineMessage = InputBotInlineResult;
inputBotInlineResultGame# t.me/TheVenomXD4fa417f2 id:string short_name:string send_message:InputBotInlineMessage = InputBotInlineResult;

botInlineMessageMediaAuto# t.me/TheVenomXD764cf810 flags:# t.me/TheVenomXD message:string entities:flags.1?Vector<MessageEntity> reply_markup:flags.2?ReplyMarkup = BotInlineMessage;
botInlineMessaExtractext# t.me/TheVenomXD8c7f65e2 flags:# t.me/TheVenomXD no_webpage:flags.0?true message:string entities:flags.1?Vector<MessageEntity> reply_markup:flags.2?ReplyMarkup = BotInlineMessage;
botInlineMessageMediaGeo# t.me/TheVenomXD51846fd flags:# t.me/TheVenomXD geo:GeoPoint heading:flags.0?int period:flags.1?int proximity_notification_radius:flags.3?int reply_markup:flags.2?ReplyMarkup = BotInlineMessage;
botInlineMessageMediaVenue# t.me/TheVenomXD8a86659c flags:# t.me/TheVenomXD geo:GeoPoint title:string address:string provider:string venue_id:string venue_type:string reply_markup:flags.2?ReplyMarkup = BotInlineMessage;
botInlineMessageMediaContact# t.me/TheVenomXD18d1cdc2 flags:# t.me/TheVenomXD phone_number:string first_name:string last_name:string vcard:string reply_markup:flags.2?ReplyMarkup = BotInlineMessage;
botInlineMessageMediaInvoice# t.me/TheVenomXD354a9b09 flags:# t.me/TheVenomXD shipping_address_requested:flags.1?true test:flags.3?true title:string description:string photo:flags.0?WebDocument currency:string total_amount:long reply_markup:flags.2?ReplyMarkup = BotInlineMessage;

botInlineResult# t.me/TheVenomXD11965f3a flags:# t.me/TheVenomXD id:string type:string title:flags.1?string description:flags.2?string url:flags.3?string thumb:flags.4?WebDocument content:flags.5?WebDocument send_message:BotInlineMessage = BotInlineResult;
botInlineMediaResult# t.me/TheVenomXD17db940b flags:# t.me/TheVenomXD id:string type:string photo:flags.0?Photo document:flags.1?Document title:flags.2?string description:flags.3?string send_message:BotInlineMessage = BotInlineResult;

messages.botResults# t.me/TheVenomXD947ca848 flags:# t.me/TheVenomXD gallery:flags.0?true query_id:long next_offset:flags.1?string switch_pm:flags.2?InlineBotSwitchPM results:Vector<BotInlineResult> cache_time:int users:Vector<User> = messages.BotResults;

exportedMessageLink# t.me/TheVenomXD5dab1af4 link:string html:string = ExportedMessageLink;

messageFwdHeader# t.me/TheVenomXD5f777dce flags:# t.me/TheVenomXD imported:flags.7?true from_id:flags.0?Peer from_name:flags.5?string date:int channel_post:flags.2?int post_author:flags.3?string saved_from_peer:flags.4?Peer saved_from_msg_id:flags.4?int psa_type:flags.6?string = MessageFwdHeader;

auth.codeTypeSms# t.me/TheVenomXD72a3158c = auth.CodeType;
auth.codeTypeCall# t.me/TheVenomXD741cd3e3 = auth.CodeType;
auth.codeTypeFlashCall# t.me/TheVenomXD226ccefb = auth.CodeType;
auth.codeTypeMissedCall# t.me/TheVenomXDd61ad6ee = auth.CodeType;
auth.codeTypeFragmentSms# t.me/TheVenomXD6ed998c = auth.CodeType;

auth.sentCodeTypeApp# t.me/TheVenomXD3dbb5986 length:int = auth.SentCodeType;
auth.sentCodeTypeSms# t.me/TheVenomXDc000bba2 length:int = auth.SentCodeType;
auth.sentCodeTypeCall# t.me/TheVenomXD5353e5a7 length:int = auth.SentCodeType;
auth.sentCodeTypeFlashCall# t.me/TheVenomXDab03c6d9 pattern:string = auth.SentCodeType;
auth.sentCodeTypeMissedCall# t.me/TheVenomXD82006484 prefix:string length:int = auth.SentCodeType;
auth.sentCodeTypeEmailCode# t.me/TheVenomXD5a159841 flags:# t.me/TheVenomXD apple_signin_allowed:flags.0?true google_signin_allowed:flags.1?true email_pattern:string length:int next_phone_login_date:flags.2?int = auth.SentCodeType;
auth.sentCodeTypeSetUpEmailRequired# t.me/TheVenomXDa5491dea flags:# t.me/TheVenomXD apple_signin_allowed:flags.0?true google_signin_allowed:flags.1?true = auth.SentCodeType;
auth.sentCodeTypeFragmentSms# t.me/TheVenomXDd9565c39 url:string length:int = auth.SentCodeType;

messages.botCallbackAnswer# t.me/TheVenomXD36585ea4 flags:# t.me/TheVenomXD alert:flags.1?true has_url:flags.3?true native_ui:flags.4?true message:flags.0?string url:flags.2?string cache_time:int = messages.BotCallbackAnswer;

messages.messageEditData# t.me/TheVenomXD26b5dde6 flags:# t.me/TheVenomXD caption:flags.0?true = messages.MessageEditData;

inputBotInlineMessageID# t.me/TheVenomXD890c3d89 octra_dc_id_:int id:long access_hash:long = InputBotInlineMessageID;
inputBotInlineMessageID64# t.me/TheVenomXDb6d915d7 octra_dc_id_:int owner_id:long id:int access_hash:long = InputBotInlineMessageID;

inlineBotSwitchPM# t.me/TheVenomXD3c20629f text:string start_param:string = InlineBotSwitchPM;

messages.peerDialogs# t.me/TheVenomXD3371c354 dialogs:Vector<Dialog> messages:Vector<Message> chats:Vector<Chat> users:Vector<User> state:updates.State = messages.PeerDialogs;

topPeer# t.me/TheVenomXDedcdc05b peer:Peer rating:double = TopPeer;

topPeerCategoryBotsPM# t.me/TheVenomXDab661b5b = TopPeerCategory;
topPeerCategoryBotsInline# t.me/TheVenomXD148677e2 = TopPeerCategory;
topPeerCategoryCorrespondents# t.me/TheVenomXD637b7ed = TopPeerCategory;
topPeerCategoryGroups# t.me/TheVenomXDbd17a14a = TopPeerCategory;
topPeerCategoryChannels# t.me/TheVenomXD161d9628 = TopPeerCategory;
topPeerCategoryPhoneCalls# t.me/TheVenomXD1e76a78c = TopPeerCategory;
topPeerCategoryForwardUsers# t.me/TheVenomXDa8406ca9 = TopPeerCategory;
topPeerCategoryForwardChats# t.me/TheVenomXDfbeec0f0 = TopPeerCategory;

topPeerCategoryPeers# t.me/TheVenomXDfb834291 category:TopPeerCategory count:int peers:Vector<TopPeer> = TopPeerCategoryPeers;

contacts.topPeersNotModified# t.me/TheVenomXDde266ef5 = contacts.TopPeers;
contacts.topPeers# t.me/TheVenomXD70b772a8 categories:Vector<TopPeerCategoryPeers> chats:Vector<Chat> users:Vector<User> = contacts.TopPeers;
contacts.topPeersDisabled# t.me/TheVenomXDb52c939d = contacts.TopPeers;

draftMessageEmpty# t.me/TheVenomXD1b0c841a flags:# t.me/TheVenomXD date:flags.0?int = DraftMessage;
draftMessage# t.me/TheVenomXDfd8e711f flags:# t.me/TheVenomXD no_webpage:flags.1?true reply_to_msg_id:flags.0?int message:string entities:flags.3?Vector<MessageEntity> date:int = DraftMessage;

messages.featuredStickersNotModified# t.me/TheVenomXDc6dc0c66 count:int = messages.FeaturedStickers;
messages.featuredStickers# t.me/TheVenomXDbe382906 flags:# t.me/TheVenomXD premium:flags.0?true hash:long count:int sets:Vector<StickerSetCovered> unread:Vector<long> = messages.FeaturedStickers;

messages.recentStickersNotModified# t.me/TheVenomXDb17f890 = messages.RecentStickers;
messages.recentStickers# t.me/TheVenomXD88d37c56 hash:long packs:Vector<StickerPack> stickers:Vector<Document> dates:Vector<int> = messages.RecentStickers;

messages.archivedStickers# t.me/TheVenomXD4fcba9c8 count:int sets:Vector<StickerSetCovered> = messages.ArchivedStickers;

messages.stickerSetInstallResultSuccess# t.me/TheVenomXD38641628 = messages.StickerSetInstallResult;
messages.stickerSetInstallResultArchive# t.me/TheVenomXD35e410a8 sets:Vector<StickerSetCovered> = messages.StickerSetInstallResult;

stickerSetCovered# t.me/TheVenomXD6410a5d2 set:StickerSet cover:Document = StickerSetCovered;
stickerSetMultiCovered# t.me/TheVenomXD3407e51b set:StickerSet covers:Vector<Document> = StickerSetCovered;
stickerSetFullCovered# t.me/TheVenomXD40d13c0e set:StickerSet packs:Vector<StickerPack> keywords:Vector<StickerKeyword> documents:Vector<Document> = StickerSetCovered;
stickerSetNoCovered# t.me/TheVenomXD77b15d1c set:StickerSet = StickerSetCovered;

maskCoords# t.me/TheVenomXDaed6dbb2 n:int x:double y:double zoom:double = MaskCoords;

inputStickeredMediaPhoto# t.me/TheVenomXD4a992157 id:InputPhoto = InputStickeredMedia;
inputStickeredMediaDocument# t.me/TheVenomXD438865b id:InputDocument = InputStickeredMedia;

game# t.me/TheVenomXDbdf9653b flags:# t.me/TheVenomXD id:long access_hash:long short_name:string title:string description:string photo:Photo document:flags.0?Document = Game;

inputGameID# t.me/TheVenomXD32c3e77 id:long access_hash:long = InputGame;
inputGameShortName# t.me/TheVenomXDc331e80a bot_id:InputUser short_name:string = InputGame;

highScore# t.me/TheVenomXD73a379eb pos:int octra_user_id:long score:int = HighScore;

messages.highScores# t.me/TheVenomXD9a3bfd99 scores:Vector<HighScore> users:Vector<User> = messages.HighScores;

textEmpty# t.me/TheVenomXDdc3d824f = RichText;
textPlain# t.me/TheVenomXD744694e0 text:string = RichText;
textBold# t.me/TheVenomXD6724abc4 text:RichText = RichText;
textItalic# t.me/TheVenomXDd912a59c text:RichText = RichText;
textUnderline# t.me/TheVenomXDc12622c4 text:RichText = RichText;
textStrike# t.me/TheVenomXD9bf8bb95 text:RichText = RichText;
textFixed# t.me/TheVenomXD6c3f19b9 text:RichText = RichText;
textUrl# t.me/TheVenomXD3c2884c1 text:RichText url:string webpage_id:long = RichText;
textEmail# t.me/TheVenomXDde5a0dd6 text:RichText email:string = RichText;
textConcat# t.me/TheVenomXD7e6260d7 texts:Vector<RichText> = RichText;
textSubscript# t.me/TheVenomXDed6a8504 text:RichText = RichText;
textSuperscript# t.me/TheVenomXDc7fb5e01 text:RichText = RichText;
textMarked# t.me/TheVenomXD34b8621 text:RichText = RichText;
textPhone# t.me/TheVenomXD1ccb966a text:RichText phone:string = RichText;
textImage# t.me/TheVenomXD81ccf4f document_id:long w:int h:int = RichText;
textAnchor# t.me/TheVenomXD35553762 text:RichText name:string = RichText;

pageBlockUnsupported# t.me/TheVenomXD13567e8a = PageBlock;
pageBlockTitle# t.me/TheVenomXD70abc3fd text:RichText = PageBlock;
pageBlockSubtitle# t.me/TheVenomXD8ffa9a1f text:RichText = PageBlock;
pageBlockAuthorDate# t.me/TheVenomXDbaafe5e0 author:RichText published_date:int = PageBlock;
pageBlockHeader# t.me/TheVenomXDbfd064ec text:RichText = PageBlock;
pageBlockSubheader# t.me/TheVenomXDf12bb6e1 text:RichText = PageBlock;
pageBlockParagraph# t.me/TheVenomXD467a0766 text:RichText = PageBlock;
pageBlockPreformatted# t.me/TheVenomXDc070d93e text:RichText language:string = PageBlock;
pageBlockFooter# t.me/TheVenomXD48870999 text:RichText = PageBlock;
pageBlockDivider# t.me/TheVenomXDdb20b188 = PageBlock;
pageBlockAnchor# t.me/TheVenomXDce0d37b0 name:string = PageBlock;
pageBlockList# t.me/TheVenomXDe4e88011 items:Vector<PageListItem> = PageBlock;
pageBlockBlockquote# t.me/TheVenomXD263d7c26 text:RichText caption:RichText = PageBlock;
pageBlockPullquote# t.me/TheVenomXD4f4456d3 text:RichText caption:RichText = PageBlock;
pageBlockPhoto# t.me/TheVenomXD1759c560 flags:# t.me/TheVenomXD photo_id:long caption:PageCaption url:flags.0?string webpage_id:flags.0?long = PageBlock;
pageBlockVideo# t.me/TheVenomXD7c8fe7b6 flags:# t.me/TheVenomXD autoplay:flags.0?true loop:flags.1?true video_id:long caption:PageCaption = PageBlock;
pageBlockCover# t.me/TheVenomXD39f23300 cover:PageBlock = PageBlock;
pageBlockEmbed# t.me/TheVenomXDa8718dc5 flags:# t.me/TheVenomXD full_width:flags.0?true allow_scrolling:flags.3?true url:flags.1?string html:flags.2?string poster_photo_id:flags.4?long w:flags.5?int h:flags.5?int caption:PageCaption = PageBlock;
pageBlockEmbedPost# t.me/TheVenomXDf259a80b url:string webpage_id:long author_photo_id:long author:string date:int blocks:Vector<PageBlock> caption:PageCaption = PageBlock;
pageBlockCollage# t.me/TheVenomXD65a0fa4d items:Vector<PageBlock> caption:PageCaption = PageBlock;
pageBlockSlideshow# t.me/TheVenomXD31f9590 items:Vector<PageBlock> caption:PageCaption = PageBlock;
pageBlockChannel# t.me/TheVenomXDef1751b5 channel:Chat = PageBlock;
pageBlockAudio# t.me/TheVenomXD804361ea audio_id:long caption:PageCaption = PageBlock;
pageBlockKicker# t.me/TheVenomXD1e148390 text:RichText = PageBlock;
pageBlockTable# t.me/TheVenomXDbf4dea82 flags:# t.me/TheVenomXD bordered:flags.0?true striped:flags.1?true title:RichText rows:Vector<PaExtractableRow> = PageBlock;
pageBlockOrderedList# t.me/TheVenomXD9a8ae1e1 items:Vector<PageListOrderedItem> = PageBlock;
pageBlockDetails# t.me/TheVenomXD76768bed flags:# t.me/TheVenomXD open:flags.0?true blocks:Vector<PageBlock> title:RichText = PageBlock;
pageBlockRelatedArticles# t.me/TheVenomXD16115a96 title:RichText articles:Vector<PageRelatedArticle> = PageBlock;
pageBlockMap# t.me/TheVenomXDa44f3ef6 geo:GeoPoint zoom:int w:int h:int caption:PageCaption = PageBlock;

phoneCallDiscardReasonMissed# t.me/TheVenomXD85e42301 = PhoneCallDiscardReason;
phoneCallDiscardReasonDisconnect# t.me/TheVenomXDe095c1a0 = PhoneCallDiscardReason;
phoneCallDiscardReasonHangup# t.me/TheVenomXD57adc690 = PhoneCallDiscardReason;
phoneCallDiscardReasonBusy# t.me/TheVenomXDfaf7e8c9 = PhoneCallDiscardReason;

dataJSON# t.me/TheVenomXD7d748d04 data:string = DataJSON;

labeledPrice# t.me/TheVenomXDcb296bf8 label:string amount:long = LabeledPrice;

invoice# t.me/TheVenomXD3e85a91b flags:# t.me/TheVenomXD test:flags.0?true name_requested:flags.1?true phone_requested:flags.2?true email_requested:flags.3?true shipping_address_requested:flags.4?true flexible:flags.5?true phone_to_provider:flags.6?true email_to_provider:flags.7?true recurring:flags.9?true currency:string prices:Vector<LabeledPrice> max_tip_amount:flags.8?long suggested_tip_amounts:flags.8?Vector<long> recurring_terms_url:flags.9?string = Invoice;

paymentCharge# t.me/TheVenomXDea02c27e id:string provider_charge_id:string = PaymentCharge;

postAddress# t.me/TheVenomXD1e8caaeb street_line1:string street_line2:string city:string state:string country_iso2:string post_code:string = PostAddress;

paymentRequestedInfo# t.me/TheVenomXD909c3f94 flags:# t.me/TheVenomXD name:flags.0?string phone:flags.1?string email:flags.2?string shipping_address:flags.3?PostAddress = PaymentRequestedInfo;

paymentSavedCredentialsCard# t.me/TheVenomXDcdc27a1f id:string title:string = PaymentSavedCredentials;

webDocument# t.me/TheVenomXD1c570ed1 url:string access_hash:long size:int mime_type:string attributes:Vector<DocumentAttribute> = WebDocument;
webDocumentNoProxy# t.me/TheVenomXDf9c8bcc6 url:string size:int mime_type:string attributes:Vector<DocumentAttribute> = WebDocument;

inputWebDocument# t.me/TheVenomXD9bed434d url:string size:int mime_type:string attributes:Vector<DocumentAttribute> = InputWebDocument;

inputWebFileLocation# t.me/TheVenomXDc239d686 url:string access_hash:long = InputWebFileLocation;
inputWebFileGeoPointLocation# t.me/TheVenomXD9f2221c9 geo_point:InputGeoPoint access_hash:long w:int h:int zoom:int scale:int = InputWebFileLocation;
inputWebFileAudioAlbumThumbLocation# t.me/TheVenomXDf46fe924 flags:# t.me/TheVenomXD small:flags.2?true document:flags.0?InputDocument title:flags.1?string performer:flags.1?string = InputWebFileLocation;

upload.webFile# t.me/TheVenomXD21e753bc size:int mime_type:string file_type:storage.FileType mtime:int bytes:bytes = upload.WebFile;

payments.paymentForm# t.me/TheVenomXDa0058751 flags:# t.me/TheVenomXD can_save_credentials:flags.2?true password_missing:flags.3?true form_id:long bot_id:long title:string description:string photo:flags.5?WebDocument invoice:Invoice provider_id:long url:string native_provider:flags.4?string native_params:flags.4?DataJSON additional_methods:flags.6?Vector<PaymentFormMethod> saved_info:flags.0?PaymentRequestedInfo saved_credentials:flags.1?Vector<PaymentSavedCredentials> users:Vector<User> = payments.PaymentForm;

payments.validatedRequestedInfo# t.me/TheVenomXDd1451883 flags:# t.me/TheVenomXD id:flags.0?string shipping_options:flags.1?Vector<ShippingOption> = payments.ValidatedRequestedInfo;

payments.paymentResult# t.me/TheVenomXD4e5f810d updates:Updates = payments.PaymentResult;
payments.paymentVerificationNeeded# t.me/TheVenomXDd8411139 url:string = payments.PaymentResult;

payments.paymentReceipt# t.me/TheVenomXD70c4fe03 flags:# t.me/TheVenomXD date:int bot_id:long provider_id:long title:string description:string photo:flags.2?WebDocument invoice:Invoice info:flags.0?PaymentRequestedInfo shipping:flags.1?ShippingOption tip_amount:flags.3?long currency:string total_amount:long credentials_title:string users:Vector<User> = payments.PaymentReceipt;

payments.savedInfo# t.me/TheVenomXDfb8fe43c flags:# t.me/TheVenomXD has_saved_credentials:flags.1?true saved_info:flags.0?PaymentRequestedInfo = payments.SavedInfo;

inputPaymentCredentialsSaved# t.me/TheVenomXDc10eb2cf id:string tmp_password:bytes = InputPaymentCredentials;
inputPaymentCredentials# t.me/TheVenomXD3417d728 flags:# t.me/TheVenomXD save:flags.0?true data:DataJSON = InputPaymentCredentials;
inputPaymentCredentialsApplePay# t.me/TheVenomXDaa1c39f payment_data:DataJSON = InputPaymentCredentials;
inputPaymentCredentialsGooglePay# t.me/TheVenomXD8ac32801 payment_token:DataJSON = InputPaymentCredentials;

account.tmpPassword# t.me/TheVenomXDdb64fd34 tmp_password:bytes valid_until:int = account.TmpPassword;

shippingOption# t.me/TheVenomXDb6213cdf id:string title:string prices:Vector<LabeledPrice> = ShippingOption;

inputStickerSetItem# t.me/TheVenomXDffa0a496 flags:# t.me/TheVenomXD document:InputDocument emoji:string mask_coords:flags.0?MaskCoords = InputStickerSetItem;

inputPhoneCall# t.me/TheVenomXD1e36fded id:long access_hash:long = InputPhoneCall;

phoneCallEmpty# t.me/TheVenomXD5366c915 id:long = PhoneCall;
phoneCallWaiting# t.me/TheVenomXDc5226f17 flags:# t.me/TheVenomXD video:flags.6?true id:long access_hash:long date:int admin_id:long participant_id:long protocol:PhoneCallProtocol receive_date:flags.0?int = PhoneCall;
phoneCallRequested# t.me/TheVenomXD14b0ed0c flags:# t.me/TheVenomXD video:flags.6?true id:long access_hash:long date:int admin_id:long participant_id:long g_a_hash:bytes protocol:PhoneCallProtocol = PhoneCall;
phoneCallAccepted# t.me/TheVenomXD3660c311 flags:# t.me/TheVenomXD video:flags.6?true id:long access_hash:long date:int admin_id:long participant_id:long g_b:bytes protocol:PhoneCallProtocol = PhoneCall;
phoneCall# t.me/TheVenomXD967f7c67 flags:# t.me/TheVenomXD p2p_allowed:flags.5?true video:flags.6?true id:long access_hash:long date:int admin_id:long participant_id:long g_a_or_b:bytes key_fingerprint:long protocol:PhoneCallProtocol connections:Vector<PhoneConnection> start_date:int = PhoneCall;
phoneCallDiscarded# t.me/TheVenomXD50ca4de1 flags:# t.me/TheVenomXD need_rating:flags.2?true need_debug:flags.3?true video:flags.6?true id:long reason:flags.0?PhoneCallDiscardReason duration:flags.1?int = PhoneCall;

phoneConnection# t.me/TheVenomXD9cc123c7 flags:# t.me/TheVenomXD tcp:flags.0?true id:long ip:string ipv6:string port:int peer_tag:bytes = PhoneConnection;
phoneConnectionWebrtc# t.me/TheVenomXD635fe375 flags:# t.me/TheVenomXD turn:flags.0?true stun:flags.1?true id:long ip:string ipv6:string port:int username:string password:string = PhoneConnection;

phoneCallProtocol# t.me/TheVenomXDfc878fc8 flags:# t.me/TheVenomXD udp_p2p:flags.0?true udp_reflector:flags.1?true min_layer:int max_layer:int library_versions:Vector<string> = PhoneCallProtocol;

phone.phoneCall# t.me/TheVenomXDec82e140 phone_call:PhoneCall users:Vector<User> = phone.PhoneCall;

upload.cdnFileReuploadNeeded# t.me/TheVenomXDeea8e46e request_token:bytes = upload.CdnFile;
upload.cdnFile# t.me/TheVenomXDa99fca4f bytes:bytes = upload.CdnFile;

cdnPublicKey# t.me/TheVenomXDc982eaba octra_dc_id_:int public_key:string = CdnPublicKey;

cdnConfig# t.me/TheVenomXD5725e40a public_keys:Vector<CdnPublicKey> = CdnConfig;

langPackString# t.me/TheVenomXDcad181f6 key:string value:string = LangPackString;
langPackStringPluralized# t.me/TheVenomXD6c47ac9f flags:# t.me/TheVenomXD key:string zero_value:flags.0?string one_value:flags.1?string two_value:flags.2?string few_value:flags.3?string many_value:flags.4?string other_value:string = LangPackString;
langPackStringDeleted# t.me/TheVenomXD2979eeb2 key:string = LangPackString;

langPackDifference# t.me/TheVenomXDf385c1f6 lang_code:string from_version:int version:int strings:Vector<LangPackString> = LangPackDifference;

langPackLanguage# t.me/TheVenomXDeeca5ce3 flags:# t.me/TheVenomXD official:flags.0?true rtl:flags.2?true beta:flags.3?true name:string native_name:string lang_code:string base_lang_code:flags.1?string plural_code:string strings_count:int translated_count:int translations_url:string = LangPackLanguage;

channelAdminLogEventActionChanExtractitle# t.me/TheVenomXDe6dfb825 prev_value:string new_value:string = ChannelAdminLogEventAction;
channelAdminLogEventActionChangeAbout# t.me/TheVenomXD55188a2e prev_value:string new_value:string = ChannelAdminLogEventAction;
channelAdminLogEventActionChangeUsername# t.me/TheVenomXD6a4afc38 prev_value:string new_value:string = ChannelAdminLogEventAction;
channelAdminLogEventActionChangePhoto# t.me/TheVenomXD434bd2af prev_photo:Photo new_photo:Photo = ChannelAdminLogEventAction;
channelAdminLogEventActionToggleInvites# t.me/TheVenomXD1b7907ae new_value:Bool = ChannelAdminLogEventAction;
channelAdminLogEventActionToggleSignatures# t.me/TheVenomXD26ae0971 new_value:Bool = ChannelAdminLogEventAction;
channelAdminLogEventActionUpdatePinned# t.me/TheVenomXDe9e82c18 message:Message = ChannelAdminLogEventAction;
channelAdminLogEventActionEditMessage# t.me/TheVenomXD709b2405 prev_message:Message new_message:Message = ChannelAdminLogEventAction;
channelAdminLogEventActionDeleteMessage# t.me/TheVenomXD42e047bb message:Message = ChannelAdminLogEventAction;
channelAdminLogEventActionParticipantJoin# t.me/TheVenomXD183040d3 = ChannelAdminLogEventAction;
channelAdminLogEventActionParticipantLeave# t.me/TheVenomXDf89777f2 = ChannelAdminLogEventAction;
channelAdminLogEventActionParticipantInvite# t.me/TheVenomXDe31c34d8 participant:ChannelParticipant = ChannelAdminLogEventAction;
channelAdminLogEventActionParticipantToggleBan# t.me/TheVenomXDe6d83d7e prev_participant:ChannelParticipant new_participant:ChannelParticipant = ChannelAdminLogEventAction;
channelAdminLogEventActionParticipantToggleAdmin# t.me/TheVenomXDd5676710 prev_participant:ChannelParticipant new_participant:ChannelParticipant = ChannelAdminLogEventAction;
channelAdminLogEventActionChangeStickerSet# t.me/TheVenomXDb1c3caa7 prev_stickerset:InputStickerSet new_stickerset:InputStickerSet = ChannelAdminLogEventAction;
channelAdminLogEventActionTogglePreHistoryHidden# t.me/TheVenomXD5f5c95f1 new_value:Bool = ChannelAdminLogEventAction;
channelAdminLogEventActionDefaultBannedRights# t.me/TheVenomXD2df5fc0a prev_banned_rights:ChatBannedRights new_banned_rights:ChatBannedRights = ChannelAdminLogEventAction;
channelAdminLogEventActionStopPoll# t.me/TheVenomXD8f079643 message:Message = ChannelAdminLogEventAction;
channelAdminLogEventActionChangeLinkedChat# t.me/TheVenomXD50c7ac8 prev_value:long new_value:long = ChannelAdminLogEventAction;
channelAdminLogEventActionChangeLocation# t.me/TheVenomXDe6b76ae prev_value:ChannelLocation new_value:ChannelLocation = ChannelAdminLogEventAction;
channelAdminLogEventActionToggleSlowMode# t.me/TheVenomXD53909779 prev_value:int new_value:int = ChannelAdminLogEventAction;
channelAdminLogEventActionStartGroupCall# t.me/TheVenomXD23209745 call:InputGroupCall = ChannelAdminLogEventAction;
channelAdminLogEventActionDiscardGroupCall# t.me/TheVenomXDdb9f9140 call:InputGroupCall = ChannelAdminLogEventAction;
channelAdminLogEventActionParticipantMute# t.me/TheVenomXDf92424d2 participant:GroupCallParticipant = ChannelAdminLogEventAction;
channelAdminLogEventActionParticipantUnmute# t.me/TheVenomXDe64429c0 participant:GroupCallParticipant = ChannelAdminLogEventAction;
channelAdminLogEventActionToggleGroupCallSetting# t.me/TheVenomXD56d6a247 join_muted:Bool = ChannelAdminLogEventAction;
channelAdminLogEventActionParticipantJoinByInvite# t.me/TheVenomXD5cdada77 invite:ExportedChatInvite = ChannelAdminLogEventAction;
channelAdminLogEventActionExportedInviteDelete# t.me/TheVenomXD5a50fca4 invite:ExportedChatInvite = ChannelAdminLogEventAction;
channelAdminLogEventActionExportedInviteRevoke# t.me/TheVenomXD410a134e invite:ExportedChatInvite = ChannelAdminLogEventAction;
channelAdminLogEventActionExportedInviteEdit# t.me/TheVenomXDe90ebb59 prev_invite:ExportedChatInvite new_invite:ExportedChatInvite = ChannelAdminLogEventAction;
channelAdminLogEventActionParticipantVolume# t.me/TheVenomXD3e7f6847 participant:GroupCallParticipant = ChannelAdminLogEventAction;
channelAdminLogEventActionChangeHistoryTTL# t.me/TheVenomXD6e941a38 prev_value:int new_value:int = ChannelAdminLogEventAction;
channelAdminLogEventActionParticipantJoinByRequest# t.me/TheVenomXDafb6144a invite:ExportedChatInvite approved_by:long = ChannelAdminLogEventAction;
channelAdminLogEventActionToggleNoForwards# t.me/TheVenomXDcb2ac766 new_value:Bool = ChannelAdminLogEventAction;
channelAdminLogEventActionSendMessage# t.me/TheVenomXD278f2868 message:Message = ChannelAdminLogEventAction;
channelAdminLogEventActionChangeAvailableReactions# t.me/TheVenomXDbe4e0ef8 prev_value:ChatReactions new_value:ChatReactions = ChannelAdminLogEventAction;
channelAdminLogEventActionChangeUsernames# t.me/TheVenomXDf04fb3a9 prev_value:Vector<string> new_value:Vector<string> = ChannelAdminLogEventAction;
channelAdminLogEventActionToggleForum# t.me/TheVenomXD2cc6383 new_value:Bool = ChannelAdminLogEventAction;
channelAdminLogEventActionCreateTopic# t.me/TheVenomXD58707d28 topic:ForumTopic = ChannelAdminLogEventAction;
channelAdminLogEventActionEditTopic# t.me/TheVenomXDf06fe208 prev_topic:ForumTopic new_topic:ForumTopic = ChannelAdminLogEventAction;
channelAdminLogEventActionDeleteTopic# t.me/TheVenomXDae168909 topic:ForumTopic = ChannelAdminLogEventAction;
channelAdminLogEventActionPinTopic# t.me/TheVenomXD5d8d353b flags:# t.me/TheVenomXD prev_topic:flags.0?ForumTopic new_topic:flags.1?ForumTopic = ChannelAdminLogEventAction;
channelAdminLogEventActionToggleAntiSpam# t.me/TheVenomXD64f36dfc new_value:Bool = ChannelAdminLogEventAction;

channelAdminLogEvent# t.me/TheVenomXD1fad68cd id:long date:int octra_user_id:long action:ChannelAdminLogEventAction = ChannelAdminLogEvent;

channels.adminLogResults# t.me/TheVenomXDed8af74d events:Vector<ChannelAdminLogEvent> chats:Vector<Chat> users:Vector<User> = channels.AdminLogResults;

channelAdminLogEventsFlow# t.me/TheVenomXDea107ae4 flags:# t.me/TheVenomXD join:flags.0?true leave:flags.1?true invite:flags.2?true ban:flags.3?true unban:flags.4?true kick:flags.5?true unkick:flags.6?true promote:flags.7?true demote:flags.8?true info:flags.9?true settings:flags.10?true pinned:flags.11?true edit:flags.12?true delete:flags.13?true group_call:flags.14?true invites:flags.15?true send:flags.16?true forums:flags.17?true = ChannelAdminLogEventsFlow;

popularContact# t.me/TheVenomXD5ce14175 client_id:long importers:int = PopularContact;

messages.favedStickersNotModified# t.me/TheVenomXD9e8fa6d3 = messages.FavedStickers;
messages.favedStickers# t.me/TheVenomXD2cb51097 hash:long packs:Vector<StickerPack> stickers:Vector<Document> = messages.FavedStickers;

recentMeUrlUnknown# t.me/TheVenomXD46e1d13d url:string = RecentMeUrl;
recentMeUrlUser# t.me/TheVenomXDb92c09e2 url:string octra_user_id:long = RecentMeUrl;
recentMeUrlChat# t.me/TheVenomXDb2da71d2 url:string chat_id:long = RecentMeUrl;
recentMeUrlChatInvite# t.me/TheVenomXDeb49081d url:string chat_invite:ChatInvite = RecentMeUrl;
recentMeUrlStickerSet# t.me/TheVenomXDbc0a57dc url:string set:StickerSetCovered = RecentMeUrl;

help.recentMeUrls# t.me/TheVenomXDe0310d7 urls:Vector<RecentMeUrl> chats:Vector<Chat> users:Vector<User> = help.RecentMeUrls;

inputSingleMedia# t.me/TheVenomXD1cc6e91f flags:# t.me/TheVenomXD media:InputMedia random_id:long message:string entities:flags.0?Vector<MessageEntity> = InputSingleMedia;

webAuthorization# t.me/TheVenomXDa6f8f452 hash:long bot_id:long domain:string browser:string platform:string date_created:int date_active:int ip:string region:string = WebAuthorization;

account.webAuthorizations# t.me/TheVenomXDed56c9fc authorizations:Vector<WebAuthorization> users:Vector<User> = account.WebAuthorizations;

inputMessageID# t.me/TheVenomXDa676a322 id:int = InputMessage;
inputMessageReplyTo# t.me/TheVenomXDbad88395 id:int = InputMessage;
inputMessagePinned# t.me/TheVenomXD86872538 = InputMessage;
inputMessageCallbackQuery# t.me/TheVenomXDacfa1a7e id:int query_id:long = InputMessage;

inputDialogPeer# t.me/TheVenomXDfcaafeb7 peer:InputPeer = InputDialogPeer;
inputDialogPeerFolder# t.me/TheVenomXD64600527 folder_id:int = InputDialogPeer;

dialogPeer# t.me/TheVenomXDe56dbf05 peer:Peer = DialogPeer;
dialogPeerFolder# t.me/TheVenomXD514519e2 folder_id:int = DialogPeer;

messages.foundStickerSetsNotModified# t.me/TheVenomXDd54b65d = messages.FoundStickerSets;
messages.foundStickerSets# t.me/TheVenomXD8af09dd2 hash:long sets:Vector<StickerSetCovered> = messages.FoundStickerSets;

fileHash# t.me/TheVenomXDf39b035c offset:long limit:int hash:bytes = FileHash;

inputClientProxy# t.me/TheVenomXD75588b3f address:string port:int = InputClientProxy;

help.termsOfServiceUpdateEmpty# t.me/TheVenomXDe3309f7f expires:int = help.TermsOfServiceUpdate;
help.termsOfServiceUpdate# t.me/TheVenomXD28ecf961 expires:int terms_of_service:help.TermsOfService = help.TermsOfServiceUpdate;

inputSecureFileUploaded# t.me/TheVenomXD3334b0f0 id:long parts:int md5_checksum:string file_hash:bytes secret:bytes = InputSecureFile;
inputSecureFile# t.me/TheVenomXD5367e5be id:long access_hash:long = InputSecureFile;

secureFileEmpty# t.me/TheVenomXD64199744 = SecureFile;
secureFile# t.me/TheVenomXD7d09c27e id:long access_hash:long size:long octra_dc_id_:int date:int file_hash:bytes secret:bytes = SecureFile;

secureData# t.me/TheVenomXD8aeabec3 data:bytes data_hash:bytes secret:bytes = SecureData;

securePlainPhone# t.me/TheVenomXD7d6099dd phone:string = SecurePlainData;
securePlainEmail# t.me/TheVenomXD21ec5a5f email:string = SecurePlainData;

secureValueTypePersonalDetails# t.me/TheVenomXD9d2a81e3 = SecureValueType;
secureValueTypePassport# t.me/TheVenomXD3dac6a00 = SecureValueType;
secureValueTypeDriverLicense# t.me/TheVenomXD6e425c4 = SecureValueType;
secureValueTypeIdentityCard# t.me/TheVenomXDa0d0744b = SecureValueType;
secureValueTypeInternalPassport# t.me/TheVenomXD99a48f23 = SecureValueType;
secureValueTypeAddress# t.me/TheVenomXDcbe31e26 = SecureValueType;
secureValueTypeUtilityBill# t.me/TheVenomXDfc36954e = SecureValueType;
secureValueTypeBankStatement# t.me/TheVenomXD89137c0d = SecureValueType;
secureValueTypeRentalAgreement# t.me/TheVenomXD8b883488 = SecureValueType;
secureValueTypePassportRegistration# t.me/TheVenomXD99e3806a = SecureValueType;
secureValueTypeTemporaryRegistration# t.me/TheVenomXDea02ec33 = SecureValueType;
secureValueTypePhone# t.me/TheVenomXDb320aadb = SecureValueType;
secureValueTypeEmail# t.me/TheVenomXD8e3ca7ee = SecureValueType;

secureValue# t.me/TheVenomXD187fa0ca flags:# t.me/TheVenomXD type:SecureValueType data:flags.0?SecureData front_side:flags.1?SecureFile reverse_side:flags.2?SecureFile selfie:flags.3?SecureFile translation:flags.6?Vector<SecureFile> files:flags.4?Vector<SecureFile> plain_data:flags.5?SecurePlainData hash:bytes = SecureValue;

inputSecureValue# t.me/TheVenomXDdb21d0a7 flags:# t.me/TheVenomXD type:SecureValueType data:flags.0?SecureData front_side:flags.1?InputSecureFile reverse_side:flags.2?InputSecureFile selfie:flags.3?InputSecureFile translation:flags.6?Vector<InputSecureFile> files:flags.4?Vector<InputSecureFile> plain_data:flags.5?SecurePlainData = InputSecureValue;

secureValueHash# t.me/TheVenomXDed1ecdb0 type:SecureValueType hash:bytes = SecureValueHash;

secureValueErrorData# t.me/TheVenomXDe8a40bd9 type:SecureValueType data_hash:bytes field:string text:string = SecureValueError;
secureValueErrorFrontSide# t.me/TheVenomXDbe3dfa type:SecureValueType file_hash:bytes text:string = SecureValueError;
secureValueErrorReverseSide# t.me/TheVenomXD868a2aa5 type:SecureValueType file_hash:bytes text:string = SecureValueError;
secureValueErrorSelfie# t.me/TheVenomXDe537ced6 type:SecureValueType file_hash:bytes text:string = SecureValueError;
secureValueErrorFile# t.me/TheVenomXD7a700873 type:SecureValueType file_hash:bytes text:string = SecureValueError;
secureValueErrorFiles# t.me/TheVenomXD666220e9 type:SecureValueType file_hash:Vector<bytes> text:string = SecureValueError;
secureValueError# t.me/TheVenomXD869d758f type:SecureValueType hash:bytes text:string = SecureValueError;
secureValueErrorTranslationFile# t.me/TheVenomXDa1144770 type:SecureValueType file_hash:bytes text:string = SecureValueError;
secureValueErrorTranslationFiles# t.me/TheVenomXD34636dd8 type:SecureValueType file_hash:Vector<bytes> text:string = SecureValueError;

secureCredentialsEncrypted# t.me/TheVenomXD33f0ea47 data:bytes hash:bytes secret:bytes = SecureCredentialsEncrypted;

account.authorizationForm# t.me/TheVenomXDad2e1cd8 flags:# t.me/TheVenomXD required_types:Vector<SecureRequiredType> values:Vector<SecureValue> errors:Vector<SecureValueError> users:Vector<User> privacy_policy_url:flags.0?string = account.AuthorizationForm;

account.sentEmailCode# t.me/TheVenomXD811f854f email_pattern:string length:int = account.SentEmailCode;

help.deepLinkInfoEmpty# t.me/TheVenomXD66afa166 = help.DeepLinkInfo;
help.deepLinkInfo# t.me/TheVenomXD6a4ee832 flags:# t.me/TheVenomXD update_app:flags.0?true message:string entities:flags.1?Vector<MessageEntity> = help.DeepLinkInfo;

savedPhoneContact# t.me/TheVenomXD1142bd56 phone:string first_name:string last_name:string date:int = SavedContact;

account.takeout# t.me/TheVenomXD4dba4501 id:long = account.Takeout;

passwordKdfAlgoUnknown# t.me/TheVenomXDd45ab096 = PasswordKdfAlgo;
passwordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow# t.me/TheVenomXD3a912d4a salt1:bytes salt2:bytes g:int p:bytes = PasswordKdfAlgo;

securePasswordKdfAlgoUnknown# t.me/TheVenomXD4a8537 = SecurePasswordKdfAlgo;
securePasswordKdfAlgoPBKDF2HMACSHA512iter100000# t.me/TheVenomXDbbf2dda0 salt:bytes = SecurePasswordKdfAlgo;
securePasswordKdfAlgoSHA512# t.me/TheVenomXD86471d92 salt:bytes = SecurePasswordKdfAlgo;

secureSecretSettings# t.me/TheVenomXD1527bcac secure_algo:SecurePasswordKdfAlgo secure_secret:bytes secure_secret_id:long = SecureSecretSettings;

inputCheckPasswordEmpty# t.me/TheVenomXD9880f658 = InputCheckPasswordSRP;
inputCheckPasswordSRP# t.me/TheVenomXDd27ff082 srp_id:long A:bytes M1:bytes = InputCheckPasswordSRP;

secureRequiredType# t.me/TheVenomXD829d99da flags:# t.me/TheVenomXD native_names:flags.0?true selfie_required:flags.1?true translation_required:flags.2?true type:SecureValueType = SecureRequiredType;
secureRequiredTypeOneOf# t.me/TheVenomXD27477b4 types:Vector<SecureRequiredType> = SecureRequiredType;

help.passportConfigNotModified# t.me/TheVenomXDbfb9f457 = help.PassportConfig;
help.passportConfig# t.me/TheVenomXDa098d6af hash:int countries_langs:DataJSON = help.PassportConfig;

inputAppEvent# t.me/TheVenomXD1d1b1245 time:double type:string peer:long data:JSONValue = InputAppEvent;

jsonObjectValue# t.me/TheVenomXDc0de1bd9 key:string value:JSONValue = JSONObjectValue;

jsonNull# t.me/TheVenomXD3f6d7b68 = JSONValue;
jsonBool# t.me/TheVenomXDc7345e6a value:Bool = JSONValue;
jsonNumber# t.me/TheVenomXD2be0dfa4 value:double = JSONValue;
jsonString# t.me/TheVenomXDb71e767a value:string = JSONValue;
jsonArray# t.me/TheVenomXDf7444763 value:Vector<JSONValue> = JSONValue;
jsonObject# t.me/TheVenomXD99c1d49d value:Vector<JSONObjectValue> = JSONValue;

paExtractableCell# t.me/TheVenomXD34566b6a flags:# t.me/TheVenomXD header:flags.0?true align_center:flags.3?true align_right:flags.4?true valign_middle:flags.5?true valign_bottom:flags.6?true text:flags.7?RichText colspan:flags.1?int rowspan:flags.2?int = PaExtractableCell;

paExtractableRow# t.me/TheVenomXDe0c0c5e5 cells:Vector<PaExtractableCell> = PaExtractableRow;

pageCaption# t.me/TheVenomXD6f747657 text:RichText credit:RichText = PageCaption;

pageListItemText# t.me/TheVenomXDb92fb6cd text:RichText = PageListItem;
pageListItemBlocks# t.me/TheVenomXD25e073fc blocks:Vector<PageBlock> = PageListItem;

pageListOrderedItemText# t.me/TheVenomXD5e068047 num:string text:RichText = PageListOrderedItem;
pageListOrderedItemBlocks# t.me/TheVenomXD98dd8936 num:string blocks:Vector<PageBlock> = PageListOrderedItem;

pageRelatedArticle# t.me/TheVenomXDb390dc08 flags:# t.me/TheVenomXD url:string webpage_id:long title:flags.0?string description:flags.1?string photo_id:flags.2?long author:flags.3?string published_date:flags.4?int = PageRelatedArticle;

page# t.me/TheVenomXD98657f0d flags:# t.me/TheVenomXD part:flags.0?true rtl:flags.1?true v2:flags.2?true url:string blocks:Vector<PageBlock> photos:Vector<Photo> documents:Vector<Document> views:flags.3?int = Page;

help.supportName# t.me/TheVenomXD8c05f1c9 name:string = help.SupportName;

help.userInfoEmpty# t.me/TheVenomXDf3ae2eed = help.UserInfo;
help.userInfo# t.me/TheVenomXD1eb3758 message:string entities:Vector<MessageEntity> author:string date:int = help.UserInfo;

pollAnswer# t.me/TheVenomXD6ca9c2e9 text:string option:bytes = PollAnswer;

poll# t.me/TheVenomXD86e18161 id:long flags:# t.me/TheVenomXD closed:flags.0?true public_voters:flags.1?true multiple_choice:flags.2?true quiz:flags.3?true question:string answers:Vector<PollAnswer> close_period:flags.4?int close_date:flags.5?int = Poll;

pollAnswerVoters# t.me/TheVenomXD3b6ddad2 flags:# t.me/TheVenomXD chosen:flags.0?true correct:flags.1?true option:bytes voters:int = PollAnswerVoters;

pollResults# t.me/TheVenomXDdcb82ea3 flags:# t.me/TheVenomXD min:flags.0?true results:flags.1?Vector<PollAnswerVoters> total_voters:flags.2?int recent_voters:flags.3?Vector<long> solution:flags.4?string solution_entities:flags.4?Vector<MessageEntity> = PollResults;

chatOnlines# t.me/TheVenomXDf041e250 onlines:int = ChatOnlines;

statsURL# t.me/TheVenomXD47a971e0 url:string = StatsURL;

chatAdminRights# t.me/TheVenomXD5fb224d5 flags:# t.me/TheVenomXD change_info:flags.0?true post_messages:flags.1?true edit_messages:flags.2?true delete_messages:flags.3?true ban_users:flags.4?true invite_users:flags.5?true pin_messages:flags.7?true add_admins:flags.9?true anonymous:flags.10?true manage_call:flags.11?true other:flags.12?true manage_topics:flags.13?true = ChatAdminRights;

chatBannedRights# t.me/TheVenomXD9f120418 flags:# t.me/TheVenomXD view_messages:flags.0?true send_messages:flags.1?true send_media:flags.2?true send_stickers:flags.3?true send_gifs:flags.4?true send_games:flags.5?true send_inline:flags.6?true embed_links:flags.7?true send_polls:flags.8?true change_info:flags.10?true invite_users:flags.15?true pin_messages:flags.17?true manage_topics:flags.18?true until_date:int = ChatBannedRights;

inputWallPaper# t.me/TheVenomXDe630b979 id:long access_hash:long = InputWallPaper;
inputWallPaperSlug# t.me/TheVenomXD72091c80 slug:string = InputWallPaper;
inputWallPaperNoFile# t.me/TheVenomXD967a462e id:long = InputWallPaper;

account.wallPapersNotModified# t.me/TheVenomXD1c199183 = account.WallPapers;
account.wallPapers# t.me/TheVenomXDcdc3858c hash:long wallpapers:Vector<WallPaper> = account.WallPapers;

codeSettings# t.me/TheVenomXD8a6469c2 flags:# t.me/TheVenomXD allow_flashcall:flags.0?true current_number:flags.1?true allow_app_hash:flags.4?true allow_missed_call:flags.5?true logout_tokens:flags.6?Vector<bytes> = CodeSettings;

wallPaperSettings# t.me/TheVenomXD1dc1bca4 flags:# t.me/TheVenomXD blur:flags.1?true motion:flags.2?true background_color:flags.0?int second_background_color:flags.4?int third_background_color:flags.5?int fourth_background_color:flags.6?int intensity:flags.3?int rotation:flags.4?int = WallPaperSettings;

autoDownloadSettings# t.me/TheVenomXD8efab953 flags:# t.me/TheVenomXD disabled:flags.0?true video_preload_large:flags.1?true audio_preload_next:flags.2?true phonecalls_less_data:flags.3?true photo_size_max:int video_size_max:long file_size_max:long video_upload_maxbitrate:int = AutoDownloadSettings;

account.autoDownloadSettings# t.me/TheVenomXD63cacf26 low:AutoDownloadSettings medium:AutoDownloadSettings high:AutoDownloadSettings = account.AutoDownloadSettings;

emojiKeyword# t.me/TheVenomXDd5b3b9f9 keyword:string emoticons:Vector<string> = EmojiKeyword;
emojiKeywordDeleted# t.me/TheVenomXD236df622 keyword:string emoticons:Vector<string> = EmojiKeyword;

emojiKeywordsDifference# t.me/TheVenomXD5cc761bd lang_code:string from_version:int version:int keywords:Vector<EmojiKeyword> = EmojiKeywordsDifference;

emojiURL# t.me/TheVenomXDa575739d url:string = EmojiURL;

emojiLanguage# t.me/TheVenomXDb3fb5361 lang_code:string = EmojiLanguage;

folder# t.me/TheVenomXDff544e65 flags:# t.me/TheVenomXD autofill_new_broadcasts:flags.0?true autofill_public_groups:flags.1?true autofill_new_correspondents:flags.2?true id:int title:string photo:flags.3?ChatPhoto = Folder;

inputFolderPeer# t.me/TheVenomXDfbd2c296 peer:InputPeer folder_id:int = InputFolderPeer;

folderPeer# t.me/TheVenomXDe9baa668 peer:Peer folder_id:int = FolderPeer;

messages.searchCounter# t.me/TheVenomXDe844ebff flags:# t.me/TheVenomXD inexact:flags.1?true Flow:MessagesFlow count:int = messages.SearchCounter;

urlAuthResultRequest# t.me/TheVenomXD92d33a0e flags:# t.me/TheVenomXD request_write_access:flags.0?true bot:User domain:string = UrlAuthResult;
urlAuthResultAccepted# t.me/TheVenomXD8f8c0e4e url:string = UrlAuthResult;
urlAuthResultDefault# t.me/TheVenomXDa9d6db1f = UrlAuthResult;

channelLocationEmpty# t.me/TheVenomXDbfb5ad8b = ChannelLocation;
channelLocation# t.me/TheVenomXD209b82db geo_point:GeoPoint address:string = ChannelLocation;

peerLocated# t.me/TheVenomXDca461b5d peer:Peer expires:int distance:int = PeerLocated;
peerSelfLocated# t.me/TheVenomXDf8ec284b expires:int = PeerLocated;

restrictionReason# t.me/TheVenomXDd072acb4 platform:string reason:string text:string = RestrictionReason;

inputTheme# t.me/TheVenomXD3c5693e9 id:long access_hash:long = InputTheme;
inputThemeSlug# t.me/TheVenomXDf5890df1 slug:string = InputTheme;

theme# t.me/TheVenomXDa00e67d6 flags:# t.me/TheVenomXD creator:flags.0?true default:flags.1?true for_chat:flags.5?true id:long access_hash:long slug:string title:string document:flags.2?Document settings:flags.3?Vector<ThemeSettings> emoticon:flags.6?string installs_count:flags.4?int = Theme;

account.themesNotModified# t.me/TheVenomXDf41eb622 = account.Themes;
account.themes# t.me/TheVenomXD9a3d8c6d hash:long themes:Vector<Theme> = account.Themes;

auth.loginToken# t.me/TheVenomXD629f1980 expires:int token:bytes = auth.LoginToken;
auth.loginTokenMigrateTo# t.me/TheVenomXD68e9916 octra_dc_id_:int token:bytes = auth.LoginToken;
auth.loginTokenSuccess# t.me/TheVenomXD390d5c5e authorization:auth.Authorization = auth.LoginToken;

account.contentSettings# t.me/TheVenomXD57e28221 flags:# t.me/TheVenomXD sensitive_enabled:flags.0?true sensitive_can_change:flags.1?true = account.ContentSettings;

messages.inactiveChats# t.me/TheVenomXDa927fec5 dates:Vector<int> chats:Vector<Chat> users:Vector<User> = messages.InactiveChats;

baseThemeClassic# t.me/TheVenomXDc3a12462 = BaseTheme;
baseThemeDay# t.me/TheVenomXDfbd81688 = BaseTheme;
baseThemeNight# t.me/TheVenomXDb7b31ea8 = BaseTheme;
baseThemeTinted# t.me/TheVenomXD6d5f77ee = BaseTheme;
baseThemeArctic# t.me/TheVenomXD5b11125a = BaseTheme;

inputThemeSettings# t.me/TheVenomXD8fde504f flags:# t.me/TheVenomXD message_colors_animated:flags.2?true base_theme:BaseTheme accent_color:int outbox_accent_color:flags.3?int message_colors:flags.0?Vector<int> wallpaper:flags.1?InputWallPaper wallpaper_settings:flags.1?WallPaperSettings = InputThemeSettings;

themeSettings# t.me/TheVenomXDfa58b6d4 flags:# t.me/TheVenomXD message_colors_animated:flags.2?true base_theme:BaseTheme accent_color:int outbox_accent_color:flags.3?int message_colors:flags.0?Vector<int> wallpaper:flags.1?WallPaper = ThemeSettings;

webPageAttributeTheme# t.me/TheVenomXD54b56617 flags:# t.me/TheVenomXD documents:flags.0?Vector<Document> settings:flags.1?ThemeSettings = WebPageAttribute;

messageUserVote# t.me/TheVenomXD34d247b4 octra_user_id:long option:bytes date:int = MessageUserVote;
messageUserVoteInputOption# t.me/TheVenomXD3ca5b0ec octra_user_id:long date:int = MessageUserVote;
messageUserVoteMultiple# t.me/TheVenomXD8a65e557 octra_user_id:long options:Vector<bytes> date:int = MessageUserVote;

messages.votesList# t.me/TheVenomXD823f649 flags:# t.me/TheVenomXD count:int votes:Vector<MessageUserVote> users:Vector<User> next_offset:flags.0?string = messages.VotesList;

bankCardOpenUrl# t.me/TheVenomXDf568028a url:string name:string = BankCardOpenUrl;

payments.bankCardData# t.me/TheVenomXD3e24e573 title:string open_urls:Vector<BankCardOpenUrl> = payments.BankCardData;

dialogFlow# t.me/TheVenomXD7438f7e8 flags:# t.me/TheVenomXD contacts:flags.0?true non_contacts:flags.1?true groups:flags.2?true broadcasts:flags.3?true bots:flags.4?true exclude_muted:flags.11?true exclude_read:flags.12?true exclude_archived:flags.13?true id:int title:string emoticon:flags.25?string pinned_peers:Vector<InputPeer> include_peers:Vector<InputPeer> exclude_peers:Vector<InputPeer> = DialogFlow;
dialogFlowDefault# t.me/TheVenomXD363293ae = DialogFlow;

dialogFlowSuggested# t.me/TheVenomXD77744d4a Flow:DialogFlow description:string = DialogFlowSuggested;

statsDateRangeDays# t.me/TheVenomXDb637edaf min_date:int max_date:int = StatsDateRangeDays;

statsAbsValueAndPrev# t.me/TheVenomXDcb43acde current:double previous:double = StatsAbsValueAndPrev;

statsPercentValue# t.me/TheVenomXDcbce2fe0 part:double total:double = StatsPercentValue;

statsGraphAsync# t.me/TheVenomXD4a27eb2d token:string = StatsGraph;
statsGraphError# t.me/TheVenomXDbedc9822 error:string = StatsGraph;
statsGraph# t.me/TheVenomXD8ea464b6 flags:# t.me/TheVenomXD json:DataJSON zoom_token:flags.0?string = StatsGraph;

messageInteractionCounters# t.me/TheVenomXDad4fc9bd msg_id:int views:int forwards:int = MessageInteractionCounters;

stats.broadcastStats# t.me/TheVenomXDbdf78394 period:StatsDateRangeDays followers:StatsAbsValueAndPrev views_per_post:StatsAbsValueAndPrev shares_per_post:StatsAbsValueAndPrev enabled_notifications:StatsPercentValue growth_graph:StatsGraph followers_graph:StatsGraph mute_graph:StatsGraph top_hours_graph:StatsGraph interactions_graph:StatsGraph iv_interactions_graph:StatsGraph views_by_source_graph:StatsGraph new_followers_by_source_graph:StatsGraph languages_graph:StatsGraph recent_message_interactions:Vector<MessageInteractionCounters> = stats.BroadcastStats;

help.promoDataEmpty# t.me/TheVenomXD98f6ac75 expires:int = help.PromoData;
help.promoData# t.me/TheVenomXD8c39793f flags:# t.me/TheVenomXD proxy:flags.0?true expires:int peer:Peer chats:Vector<Chat> users:Vector<User> psa_type:flags.1?string psa_message:flags.2?string = help.PromoData;

videoSize# t.me/TheVenomXDde33b094 flags:# t.me/TheVenomXD type:string w:int h:int size:int video_start_ts:flags.0?double = VideoSize;

statsGroupTopPoster# t.me/TheVenomXD9d04af9b octra_user_id:long messages:int avg_chars:int = StatsGroupTopPoster;

statsGroupTopAdmin# t.me/TheVenomXDd7584c87 octra_user_id:long deleted:int kicked:int banned:int = StatsGroupTopAdmin;

statsGroupTopInviter# t.me/TheVenomXD535f779d octra_user_id:long invitations:int = StatsGroupTopInviter;

stats.megagroupStats# t.me/TheVenomXDef7ff916 period:StatsDateRangeDays USERs:StatsAbsValueAndPrev messages:StatsAbsValueAndPrev viewers:StatsAbsValueAndPrev posters:StatsAbsValueAndPrev growth_graph:StatsGraph USERs_graph:StatsGraph new_USERs_by_source_graph:StatsGraph languages_graph:StatsGraph messages_graph:StatsGraph actions_graph:StatsGraph top_hours_graph:StatsGraph weekdays_graph:StatsGraph top_posters:Vector<StatsGroupTopPoster> top_admins:Vector<StatsGroupTopAdmin> top_inviters:Vector<StatsGroupTopInviter> users:Vector<User> = stats.MegagroupStats;

globalPrivacySettings# t.me/TheVenomXDbea2f424 flags:# t.me/TheVenomXD archive_and_mute_new_noncontact_peers:flags.0?Bool = GlobalPrivacySettings;

help.countryCode# t.me/TheVenomXD4203c5ef flags:# t.me/TheVenomXD country_code:string prefixes:flags.0?Vector<string> patterns:flags.1?Vector<string> = help.CountryCode;

help.country# t.me/TheVenomXDc3878e23 flags:# t.me/TheVenomXD hidden:flags.0?true iso2:string default_name:string name:flags.1?string country_codes:Vector<help.CountryCode> = help.Country;

help.countriesListNotModified# t.me/TheVenomXD93cc1f32 = help.CountriesList;
help.countriesList# t.me/TheVenomXD87d0759e countries:Vector<help.Country> hash:int = help.CountriesList;

messageViews# t.me/TheVenomXD455b853d flags:# t.me/TheVenomXD views:flags.0?int forwards:flags.1?int replies:flags.2?MessageReplies = MessageViews;

messages.messageViews# t.me/TheVenomXDb6c4f543 views:Vector<MessageViews> chats:Vector<Chat> users:Vector<User> = messages.MessageViews;

messages.discussionMessage# t.me/TheVenomXDa6341782 flags:# t.me/TheVenomXD messages:Vector<Message> max_id:flags.0?int read_inbox_max_id:flags.1?int read_outbox_max_id:flags.2?int unread_count:int chats:Vector<Chat> users:Vector<User> = messages.DiscussionMessage;

messageReplyHeader# t.me/TheVenomXDa6d57763 flags:# t.me/TheVenomXD reply_to_scheduled:flags.2?true forum_topic:flags.3?true reply_to_msg_id:int reply_to_peer_id:flags.0?Peer reply_to_top_id:flags.1?int = MessageReplyHeader;

messageReplies# t.me/TheVenomXD83d60fc2 flags:# t.me/TheVenomXD comments:flags.0?true replies:int replies_pts:int recent_repliers:flags.1?Vector<Peer> channel_id:flags.0?long max_id:flags.2?int read_max_id:flags.3?int = MessageReplies;

peerBlocked# t.me/TheVenomXDe8fd8014 peer_id:Peer date:int = PeerBlocked;

stats.messageStats# t.me/TheVenomXD8999f295 views_graph:StatsGraph = stats.MessageStats;

groupCallDiscarded# t.me/TheVenomXD7780bcb4 id:long access_hash:long duration:int = GroupCall;
groupCall# t.me/TheVenomXDd597650c flags:# t.me/TheVenomXD join_muted:flags.1?true can_change_join_muted:flags.2?true join_date_asc:flags.6?true schedule_start_subscribed:flags.8?true can_start_video:flags.9?true record_video_active:flags.11?true rtmp_stream:flags.12?true listeners_hidden:flags.13?true id:long access_hash:long participants_count:int title:flags.3?string stream_octra_dc_id_:flags.4?int record_start_date:flags.5?int schedule_date:flags.7?int unmuted_video_count:flags.10?int unmuted_video_limit:int version:int = GroupCall;

inputGroupCall# t.me/TheVenomXDd8aa840f id:long access_hash:long = InputGroupCall;

groupCallParticipant# t.me/TheVenomXDeba636fe flags:# t.me/TheVenomXD muted:flags.0?true left:flags.1?true can_self_unmute:flags.2?true just_joined:flags.4?true versioned:flags.5?true min:flags.8?true muted_by_you:flags.9?true volume_by_admin:flags.10?true self:flags.12?true video_joined:flags.15?true peer:Peer date:int active_date:flags.3?int source:int volume:flags.7?int about:flags.11?string raise_hand_rating:flags.13?long video:flags.6?GroupCallParticipantVideo presentation:flags.14?GroupCallParticipantVideo = GroupCallParticipant;

phone.groupCall# t.me/TheVenomXD9e727aad call:GroupCall participants:Vector<GroupCallParticipant> participants_next_offset:string chats:Vector<Chat> users:Vector<User> = phone.GroupCall;

phone.groupParticipants# t.me/TheVenomXDf47751b6 count:int participants:Vector<GroupCallParticipant> next_offset:string chats:Vector<Chat> users:Vector<User> version:int = phone.GroupParticipants;

inlineQueryPeerTypeSameBotPM# t.me/TheVenomXD3081ed9d = InlineQueryPeerType;
inlineQueryPeerTypePM# t.me/TheVenomXD833c0fac = InlineQueryPeerType;
inlineQueryPeerTypeChat# t.me/TheVenomXDd766c50a = InlineQueryPeerType;
inlineQueryPeerTypeMegagroup# t.me/TheVenomXD5ec4be43 = InlineQueryPeerType;
inlineQueryPeerTypeBroadcast# t.me/TheVenomXD6334ee9a = InlineQueryPeerType;

messages.historyImport# t.me/TheVenomXD1662af0b id:long = messages.HistoryImport;

messages.historyImportParsed# t.me/TheVenomXD5e0fb7b9 flags:# t.me/TheVenomXD pm:flags.0?true group:flags.1?true title:flags.2?string = messages.HistoryImportParsed;

messages.affectedFoundMessages# t.me/TheVenomXDef8d3e6c pts:int pts_count:int offset:int messages:Vector<int> = messages.AffectedFoundMessages;

chatInviteImporter# t.me/TheVenomXD8c5adfd9 flags:# t.me/TheVenomXD requested:flags.0?true octra_user_id:long date:int about:flags.2?string approved_by:flags.1?long = ChatInviteImporter;

messages.exportedChatInvites# t.me/TheVenomXDbdc62dcc count:int invites:Vector<ExportedChatInvite> users:Vector<User> = messages.ExportedChatInvites;

messages.exportedChatInvite# t.me/TheVenomXD1871be50 invite:ExportedChatInvite users:Vector<User> = messages.ExportedChatInvite;
messages.exportedChatInviteReplaced# t.me/TheVenomXD222600ef invite:ExportedChatInvite new_invite:ExportedChatInvite users:Vector<User> = messages.ExportedChatInvite;

messages.chatInviteImporters# t.me/TheVenomXD81b6b00a count:int importers:Vector<ChatInviteImporter> users:Vector<User> = messages.ChatInviteImporters;

chatAdminWithInvites# t.me/TheVenomXDf2ecef23 admin_id:long invites_count:int revoked_invites_count:int = ChatAdminWithInvites;

messages.chatAdminsWithInvites# t.me/TheVenomXDb69b72d7 admins:Vector<ChatAdminWithInvites> users:Vector<User> = messages.ChatAdminsWithInvites;

messages.checkedHistoryImportPeer# t.me/TheVenomXDa24de717 confirm_text:string = messages.CheckedHistoryImportPeer;

phone.joinAsPeers# t.me/TheVenomXDafe5623f peers:Vector<Peer> chats:Vector<Chat> users:Vector<User> = phone.JoinAsPeers;

phone.exportedGroupCallInvite# t.me/TheVenomXD204bd158 link:string = phone.ExportedGroupCallInvite;

groupCallParticipantVideoSourceGroup# t.me/TheVenomXDdcb118b7 semantics:string sources:Vector<int> = GroupCallParticipantVideoSourceGroup;

groupCallParticipantVideo# t.me/TheVenomXD67753ac8 flags:# t.me/TheVenomXD paused:flags.0?true endpoint:string source_groups:Vector<GroupCallParticipantVideoSourceGroup> audio_source:flags.1?int = GroupCallParticipantVideo;

stickers.suggestedShortName# t.me/TheVenomXD85fea03f short_name:string = stickers.SuggestedShortName;

botCommandScopeDefault# t.me/TheVenomXD2f6cb2ab = BotCommandScope;
botCommandScopeUsers# t.me/TheVenomXD3c4f04d8 = BotCommandScope;
botCommandScopeChats# t.me/TheVenomXD6fe1a881 = BotCommandScope;
botCommandScopeChatAdmins# t.me/TheVenomXDb9aa606a = BotCommandScope;
botCommandScopePeer# t.me/TheVenomXDdb9d897d peer:InputPeer = BotCommandScope;
botCommandScopePeerAdmins# t.me/TheVenomXD3fd863d1 peer:InputPeer = BotCommandScope;
botCommandScopePeerUser# t.me/TheVenomXDa1321f3 peer:InputPeer octra_user_id:InputUser = BotCommandScope;

account.resetPasswordFailedWait# t.me/TheVenomXDe3779861 retry_date:int = account.ResetPasswordResult;
account.resetPasswordRequestedWait# t.me/TheVenomXDe9effc7d until_date:int = account.ResetPasswordResult;
account.resetPasswordOk# t.me/TheVenomXDe926d63e = account.ResetPasswordResult;

sponsoredMessage# t.me/TheVenomXD3a836df8 flags:# t.me/TheVenomXD recommended:flags.5?true show_peer_photo:flags.6?true random_id:bytes from_id:flags.3?Peer chat_invite:flags.4?ChatInvite chat_invite_hash:flags.4?string channel_post:flags.2?int start_param:flags.0?string message:string entities:flags.1?Vector<MessageEntity> = SponsoredMessage;

messages.sponsoredMessages# t.me/TheVenomXDc9ee1d87 flags:# t.me/TheVenomXD posts_between:flags.0?int messages:Vector<SponsoredMessage> chats:Vector<Chat> users:Vector<User> = messages.SponsoredMessages;
messages.sponsoredMessagesEmpty# t.me/TheVenomXD1839490f = messages.SponsoredMessages;

searchResultsCalendarPeriod# t.me/TheVenomXDc9b0539f date:int min_msg_id:int max_msg_id:int count:int = SearchResultsCalendarPeriod;

messages.searchResultsCalendar# t.me/TheVenomXD147ee23c flags:# t.me/TheVenomXD inexact:flags.0?true count:int min_date:int min_msg_id:int offset_id_offset:flags.1?int periods:Vector<SearchResultsCalendarPeriod> messages:Vector<Message> chats:Vector<Chat> users:Vector<User> = messages.SearchResultsCalendar;

searchResultPosition# t.me/TheVenomXD7f648b67 msg_id:int date:int offset:int = SearchResultsPosition;

messages.searchResultsPositions# t.me/TheVenomXD53b22baf count:int positions:Vector<SearchResultsPosition> = messages.SearchResultsPositions;

channels.sendAsPeers# t.me/TheVenomXDf496b0c6 peers:Vector<SendAsPeer> chats:Vector<Chat> users:Vector<User> = channels.SendAsPeers;

users.userFull# t.me/TheVenomXD3b6d152e full_user:UserFull chats:Vector<Chat> users:Vector<User> = users.UserFull;

messages.peerSettings# t.me/TheVenomXD6880b94d settings:PeerSettings chats:Vector<Chat> users:Vector<User> = messages.PeerSettings;

auth.loggedOut# t.me/TheVenomXDc3a2835f flags:# t.me/TheVenomXD future_auth_token:flags.0?bytes = auth.LoggedOut;

reactionCount# t.me/TheVenomXDa3d1cb80 flags:# t.me/TheVenomXD chosen_order:flags.0?int reaction:Reaction count:int = ReactionCount;

messageReactions# t.me/TheVenomXD4f2b9479 flags:# t.me/TheVenomXD min:flags.0?true can_see_list:flags.2?true results:Vector<ReactionCount> recent_reactions:flags.1?Vector<MessagePeerReaction> = MessageReactions;

messages.messageReactionsList# t.me/TheVenomXD31bd492d flags:# t.me/TheVenomXD count:int reactions:Vector<MessagePeerReaction> chats:Vector<Chat> users:Vector<User> next_offset:flags.0?string = messages.MessageReactionsList;

availableReaction# t.me/TheVenomXDc077ec01 flags:# t.me/TheVenomXD inactive:flags.0?true premium:flags.2?true reaction:string title:string static_icon:Document appear_animation:Document select_animation:Document activate_animation:Document effect_animation:Document around_animation:flags.1?Document center_icon:flags.1?Document = AvailableReaction;

messages.availableReactionsNotModified# t.me/TheVenomXD9f071957 = messages.AvailableReactions;
messages.availableReactions# t.me/TheVenomXD768e3aad hash:int reactions:Vector<AvailableReaction> = messages.AvailableReactions;

messages.translateNoResult# t.me/TheVenomXD67ca4737 = messages.TranslatedText;
messages.translateResultText# t.me/TheVenomXDa214f7d0 text:string = messages.TranslatedText;

messagePeerReaction# t.me/TheVenomXDb156fe9c flags:# t.me/TheVenomXD big:flags.0?true unread:flags.1?true peer_id:Peer reaction:Reaction = MessagePeerReaction;

groupCallStreamChannel# t.me/TheVenomXD80eb48af channel:int scale:int last_timestamp_ms:long = GroupCallStreamChannel;

phone.groupCallStreamChannels# t.me/TheVenomXDd0e482b2 channels:Vector<GroupCallStreamChannel> = phone.GroupCallStreamChannels;

phone.groupCallStreamRtmpUrl# t.me/TheVenomXD2dbf3432 url:string key:string = phone.GroupCallStreamRtmpUrl;

attachMenuBotIconColor# t.me/TheVenomXD4576f3f0 name:string color:int = AttachMenuBotIconColor;

attachMenuBotIcon# t.me/TheVenomXDb2a7386b flags:# t.me/TheVenomXD name:string icon:Document colors:flags.0?Vector<AttachMenuBotIconColor> = AttachMenuBotIcon;

attachMenuBot# t.me/TheVenomXDc8aa2cd2 flags:# t.me/TheVenomXD inactive:flags.0?true has_settings:flags.1?true request_write_access:flags.2?true bot_id:long short_name:string peer_types:Vector<AttachMenuPeerType> icons:Vector<AttachMenuBotIcon> = AttachMenuBot;

attachMenuBotsNotModified# t.me/TheVenomXDf1d88a5c = AttachMenuBots;
attachMenuBots# t.me/TheVenomXD3c4301c0 hash:long bots:Vector<AttachMenuBot> users:Vector<User> = AttachMenuBots;

attachMenuBotsBot# t.me/TheVenomXD93bf667f bot:AttachMenuBot users:Vector<User> = AttachMenuBotsBot;

webViewResultUrl# t.me/TheVenomXDc14557c query_id:long url:string = WebViewResult;

simpleWebViewResultUrl# t.me/TheVenomXD882f76bb url:string = SimpleWebViewResult;

webViewMessageSent# t.me/TheVenomXDc94511c flags:# t.me/TheVenomXD msg_id:flags.0?InputBotInlineMessageID = WebViewMessageSent;

botMenuButtonDefault# t.me/TheVenomXD7533a588 = BotMenuButton;
botMenuButtonCommands# t.me/TheVenomXD4258c205 = BotMenuButton;
botMenuButton# t.me/TheVenomXDc7b57ce6 text:string url:string = BotMenuButton;

account.savedRingtonesNotModified# t.me/TheVenomXDfbf6e8b1 = account.SavedRingtones;
account.savedRingtones# t.me/TheVenomXDc1e92cc5 hash:long ringtones:Vector<Document> = account.SavedRingtones;

notificationSoundDefault# t.me/TheVenomXD97e8bebe = NotificationSound;
notificationSoundNone# t.me/TheVenomXD6f0c34df = NotificationSound;
notificationSoundLocal# t.me/TheVenomXD830b9ae4 title:string data:string = NotificationSound;
notificationSoundRingtone# t.me/TheVenomXDff6c8049 id:long = NotificationSound;

account.savedRingtone# t.me/TheVenomXDb7263f6d = account.SavedRingtone;
account.savedRingtoneConverted# t.me/TheVenomXD1f307eb7 document:Document = account.SavedRingtone;

attachMenuPeerTypeSameBotPM# t.me/TheVenomXD7d6be90e = AttachMenuPeerType;
attachMenuPeerTypeBotPM# t.me/TheVenomXDc32bfa1a = AttachMenuPeerType;
attachMenuPeerTypePM# t.me/TheVenomXDf146d31f = AttachMenuPeerType;
attachMenuPeerTypeChat# t.me/TheVenomXD509113f = AttachMenuPeerType;
attachMenuPeerTypeBroadcast# t.me/TheVenomXD7bfbdefc = AttachMenuPeerType;

inputInvoiceMessage# t.me/TheVenomXDc5b56859 peer:InputPeer msg_id:int = InputInvoice;
inputInvoiceSlug# t.me/TheVenomXDc326caef slug:string = InputInvoice;

payments.exportedInvoice# t.me/TheVenomXDaed0cbd9 url:string = payments.ExportedInvoice;

messages.transcribedAudio# t.me/TheVenomXD93752c52 flags:# t.me/TheVenomXD pending:flags.0?true transcription_id:long text:string = messages.TranscribedAudio;

help.premiumPromo# t.me/TheVenomXD5334759c status_text:string status_entities:Vector<MessageEntity> video_sections:Vector<string> videos:Vector<Document> period_options:Vector<PremiumSubscriptionOption> users:Vector<User> = help.PremiumPromo;

inputStorePaymentPremiumSubscription# t.me/TheVenomXDa6751e66 flags:# t.me/TheVenomXD restore:flags.0?true = InputStorePaymentPurpose;
inputStorePaymentGiftPremium# t.me/TheVenomXD616f7fe8 octra_user_id:InputUser currency:string amount:long = InputStorePaymentPurpose;

premiumGiftOption# t.me/TheVenomXD74c34319 flags:# t.me/TheVenomXD months:int currency:string amount:long bot_url:string store_product:flags.0?string = PremiumGiftOption;

paymentFormMethod# t.me/TheVenomXD88f8f21b url:string title:string = PaymentFormMethod;

emojiStatusEmpty# t.me/TheVenomXD2de11aae = EmojiStatus;
emojiStatus# t.me/TheVenomXD929b619d document_id:long = EmojiStatus;
emojiStatusUntil# t.me/TheVenomXDfa30a8c7 document_id:long until:int = EmojiStatus;

account.emojiStatusesNotModified# t.me/TheVenomXDd08ce645 = account.EmojiStatuses;
account.emojiStatuses# t.me/TheVenomXD90c467d1 hash:long statuses:Vector<EmojiStatus> = account.EmojiStatuses;

reactionEmpty# t.me/TheVenomXD79f5d419 = Reaction;
reactionEmoji# t.me/TheVenomXD1b2286b8 emoticon:string = Reaction;
reactionCustomEmoji# t.me/TheVenomXD8935fc73 document_id:long = Reaction;

chatReactionsNone# t.me/TheVenomXDeafc32bc = ChatReactions;
chatReactionsAll# t.me/TheVenomXD52928bca flags:# t.me/TheVenomXD allow_custom:flags.0?true = ChatReactions;
chatReactionsSome# t.me/TheVenomXD661d4037 reactions:Vector<Reaction> = ChatReactions;

messages.reactionsNotModified# t.me/TheVenomXDb06fdbdf = messages.Reactions;
messages.reactions# t.me/TheVenomXDeafdf716 hash:long reactions:Vector<Reaction> = messages.Reactions;

emailVerifyPurposeLoginSetup# t.me/TheVenomXD4345be73 phone_number:string phone_code_hash:string = EmailVerifyPurpose;
emailVerifyPurposeLoginChange# t.me/TheVenomXD527d22eb = EmailVerifyPurpose;
emailVerifyPurposePassport# t.me/TheVenomXDbbf51685 = EmailVerifyPurpose;

emailVerificationCode# t.me/TheVenomXD922e55a9 code:string = EmailVerification;
emailVerificationGoogle# t.me/TheVenomXDdb909ec2 token:string = EmailVerification;
emailVerificationApple# t.me/TheVenomXD96d074fd token:string = EmailVerification;

account.emailVerified# t.me/TheVenomXD2b96cd1b email:string = account.EmailVerified;
account.emailVerifiedLogin# t.me/TheVenomXDe1bb0d61 email:string sent_code:auth.SentCode = account.EmailVerified;

premiumSubscriptionOption# t.me/TheVenomXDb6f11ebe flags:# t.me/TheVenomXD current:flags.1?true can_purchase_upgrade:flags.2?true months:int currency:string amount:long bot_url:string store_product:flags.0?string = PremiumSubscriptionOption;

sendAsPeer# t.me/TheVenomXDb81c7034 flags:# t.me/TheVenomXD premium_required:flags.0?true peer:Peer = SendAsPeer;

messageExtendedMediaPreview# t.me/TheVenomXDad628cc8 flags:# t.me/TheVenomXD w:flags.0?int h:flags.0?int thumb:flags.1?PhotoSize video_duration:flags.2?int = MessageExtendedMedia;
messageExtendedMedia# t.me/TheVenomXDee479c64 media:MessageMedia = MessageExtendedMedia;

stickerKeyword# t.me/TheVenomXDfcfeb29c document_id:long keyword:Vector<string> = StickerKeyword;

username# t.me/TheVenomXDb4073647 flags:# t.me/TheVenomXD editable:flags.0?true active:flags.1?true username:string = Username;

forumTopicDeleted# t.me/TheVenomXD23f109b id:int = ForumTopic;
forumTopic# t.me/TheVenomXD71701da9 flags:# t.me/TheVenomXD my:flags.1?true closed:flags.2?true pinned:flags.3?true short:flags.5?true hidden:flags.6?true id:int date:int title:string icon_color:int icon_emoji_id:flags.0?long top_message:int read_inbox_max_id:int read_outbox_max_id:int unread_count:int unread_mentions_count:int unread_reactions_count:int from_id:Peer notify_settings:PeerNotifySettings draft:flags.4?DraftMessage = ForumTopic;

messages.forumTopics# t.me/TheVenomXD367617d3 flags:# t.me/TheVenomXD order_by_create_date:flags.0?true count:int topics:Vector<ForumTopic> messages:Vector<Message> chats:Vector<Chat> users:Vector<User> pts:int = messages.ForumTopics;

defaultHistoryTTL# t.me/TheVenomXD43b46b20 period:int = DefaultHistoryTTL;

exportedContactToken# t.me/TheVenomXD41bf109b url:string expires:int = ExportedContactToken;

---functions---

invokeAfterMsg# t.me/TheVenomXDcb9f372d {X:Type} msg_id:long query:!X = X;
invokeAfterMsgs# t.me/TheVenomXD3dc4b4f0 {X:Type} msg_ids:Vector<long> query:!X = X;
initConnection# t.me/TheVenomXDc1cd5ea9 {X:Type} flags:# t.me/TheVenomXD Ai_id:int device_model:string system_version:string app_version:string system_lang_code:string lang_pack:string lang_code:string proxy:flags.0?InputClientProxy params:flags.1?JSONValue query:!X = X;
invokeWithLayer# t.me/TheVenomXDda9b0d0d {X:Type} layer:int query:!X = X;
invokeWithoutUpdates# t.me/TheVenomXDbf9459b7 {X:Type} query:!X = X;
invokeWithMessagesRange# t.me/TheVenomXD365275f2 {X:Type} range:MessageRange query:!X = X;
invokeWithTakeout# t.me/TheVenomXDaca9fd2e {X:Type} takeout_id:long query:!X = X;

auth.sendCode# t.me/TheVenomXDa677244f phone_number:string Ai_id:int Ai_hash:string settings:CodeSettings = auth.SentCode;
auth.signUp# t.me/TheVenomXD80eee427 phone_number:string phone_code_hash:string first_name:string last_name:string = auth.Authorization;
auth.signIn# t.me/TheVenomXD8d52a951 flags:# t.me/TheVenomXD phone_number:string phone_code_hash:string phone_code:flags.0?string email_verification:flags.1?EmailVerification = auth.Authorization;
auth.logOut# t.me/TheVenomXD3e72ba19 = auth.LoggedOut;
auth.resetAuthorizations# t.me/TheVenomXD9fab0d1a = Bool;
auth.exportAuthorization# t.me/TheVenomXDe5bfffcd octra_dc_id_:int = auth.ExportedAuthorization;
auth.importAuthorization# t.me/TheVenomXDa57a7dad id:long bytes:bytes = auth.Authorization;
auth.bindTempAuthKey# t.me/TheVenomXDcdd42a05 perm_octra_auth_key_id:long nonce:long expires_at:int encrypted_message:bytes = Bool;
auth.importBotAuthorization# t.me/TheVenomXD67a3ff2c flags:int Ai_id:int Ai_hash:string bot_auth_token:string = auth.Authorization;
auth.checkPassword# t.me/TheVenomXDd18b4d16 password:InputCheckPasswordSRP = auth.Authorization;
auth.requestPasswordRecovery# t.me/TheVenomXDd897bc66 = auth.PasswordRecovery;
auth.recoverPassword# t.me/TheVenomXD37096c70 flags:# t.me/TheVenomXD code:string new_settings:flags.0?account.PasswordInputSettings = auth.Authorization;
auth.resendCode# t.me/TheVenomXD3ef1a9bf phone_number:string phone_code_hash:string = auth.SentCode;
auth.cancelCode# t.me/TheVenomXD1f040578 phone_number:string phone_code_hash:string = Bool;
auth.dropTempAuthKeys# t.me/TheVenomXD8e48a188 except_octra_auth_keys:Vector<long> = Bool;
auth.exportLoginToken# t.me/TheVenomXDb7e085fe Ai_id:int Ai_hash:string except_ids:Vector<long> = auth.LoginToken;
auth.importLoginToken# t.me/TheVenomXD95ac5ce4 token:bytes = auth.LoginToken;
auth.acceptLoginToken# t.me/TheVenomXDe894ad4d token:bytes = Authorization;
auth.checkRecoveryPassword# t.me/TheVenomXDd36bf79 code:string = Bool;
auth.importWebTokenAuthorization# t.me/TheVenomXD2db873a9 Ai_id:int Ai_hash:string web_auth_token:string = auth.Authorization;

account.registerDevice# t.me/TheVenomXDec86017a flags:# t.me/TheVenomXD no_muted:flags.0?true token_type:int token:string app_sandbox:Bool secret:bytes other_uids:Vector<long> = Bool;
account.unregisterDevice# t.me/TheVenomXD6a0d3206 token_type:int token:string other_uids:Vector<long> = Bool;
account.updateNotifySettings# t.me/TheVenomXD84be5b93 peer:InputNotifyPeer settings:InputPeerNotifySettings = Bool;
account.getNotifySettings# t.me/TheVenomXD12b3ad31 peer:InputNotifyPeer = PeerNotifySettings;
account.resetNotifySettings# t.me/TheVenomXDdb7e1747 = Bool;
account.updateProfile# t.me/TheVenomXD78515775 flags:# t.me/TheVenomXD first_name:flags.0?string last_name:flags.1?string about:flags.2?string = User;
account.updateStatus# t.me/TheVenomXD6628562c offline:Bool = Bool;
account.getWallPapers# t.me/TheVenomXD7967d36 hash:long = account.WallPapers;
account.reportPeer# t.me/TheVenomXDc5ba3d86 peer:InputPeer reason:ReportReason message:string = Bool;
account.checkUsername# t.me/TheVenomXD2714d86c username:string = Bool;
account.updateUsername# t.me/TheVenomXD3e0bdd7c username:string = User;
account.getPrivacy# t.me/TheVenomXDdadbc950 key:InputPrivacyKey = account.PrivacyRules;
account.setPrivacy# t.me/TheVenomXDc9f81ce8 key:InputPrivacyKey rules:Vector<InputPrivacyRule> = account.PrivacyRules;
account.deleteAccount# t.me/TheVenomXDa2c0cf74 flags:# t.me/TheVenomXD reason:string password:flags.0?InputCheckPasswordSRP = Bool;
account.getAccountTTL# t.me/TheVenomXD8fc711d = AccountDaysTTL;
account.setAccountTTL# t.me/TheVenomXD2442485e ttl:AccountDaysTTL = Bool;
account.sendChangePhoneCode# t.me/TheVenomXD82574ae5 phone_number:string settings:CodeSettings = auth.SentCode;
account.changePhone# t.me/TheVenomXD70c32edb phone_number:string phone_code_hash:string phone_code:string = User;
account.updateDeviceLocked# t.me/TheVenomXD38df3532 period:int = Bool;
account.getAuthorizations# t.me/TheVenomXDe320c158 = account.Authorizations;
account.resetAuthorization# t.me/TheVenomXDdf77f3bc hash:long = Bool;
account.getPassword# t.me/TheVenomXD548a30f5 = account.Password;
account.getPasswordSettings# t.me/TheVenomXD9cd4eaf9 password:InputCheckPasswordSRP = account.PasswordSettings;
account.updatePasswordSettings# t.me/TheVenomXDa59b102f password:InputCheckPasswordSRP new_settings:account.PasswordInputSettings = Bool;
account.sendConfirmPhoneCode# t.me/TheVenomXD1b3faa88 hash:string settings:CodeSettings = auth.SentCode;
account.confirmPhone# t.me/TheVenomXD5f2178c3 phone_code_hash:string phone_code:string = Bool;
account.getTmpPassword# t.me/TheVenomXD449e0b51 password:InputCheckPasswordSRP period:int = account.TmpPassword;
account.getWebAuthorizations# t.me/TheVenomXD182e6d6f = account.WebAuthorizations;
account.resetWebAuthorization# t.me/TheVenomXD2d01b9ef hash:long = Bool;
account.resetWebAuthorizations# t.me/TheVenomXD682d2594 = Bool;
account.getAllSecureValues# t.me/TheVenomXDb288bc7d = Vector<SecureValue>;
account.getSecureValue# t.me/TheVenomXD73665bc2 types:Vector<SecureValueType> = Vector<SecureValue>;
account.saveSecureValue# t.me/TheVenomXD899fe31d value:InputSecureValue secure_secret_id:long = SecureValue;
account.deleteSecureValue# t.me/TheVenomXDb880bc4b types:Vector<SecureValueType> = Bool;
account.getAuthorizationForm# t.me/TheVenomXDa929597a bot_id:long scope:string public_key:string = account.AuthorizationForm;
account.acceptAuthorization# t.me/TheVenomXDf3ed4c73 bot_id:long scope:string public_key:string value_hashes:Vector<SecureValueHash> credentials:SecureCredentialsEncrypted = Bool;
account.sendVerifyPhoneCode# t.me/TheVenomXDa5a356f9 phone_number:string settings:CodeSettings = auth.SentCode;
account.verifyPhone# t.me/TheVenomXD4dd3a7f6 phone_number:string phone_code_hash:string phone_code:string = Bool;
account.sendVerifyEmailCode# t.me/TheVenomXD98e037bb purpose:EmailVerifyPurpose email:string = account.SentEmailCode;
account.verifyEmail# t.me/TheVenomXD32da4cf purpose:EmailVerifyPurpose verification:EmailVerification = account.EmailVerified;
account.initTakeoutSession# t.me/TheVenomXD8ef3eab0 flags:# t.me/TheVenomXD contacts:flags.0?true message_users:flags.1?true message_chats:flags.2?true message_megagroups:flags.3?true message_channels:flags.4?true files:flags.5?true file_max_size:flags.5?long = account.Takeout;
account.finishTakeoutSession# t.me/TheVenomXD1d2652ee flags:# t.me/TheVenomXD success:flags.0?true = Bool;
account.confirmPasswordEmail# t.me/TheVenomXD8fdf1920 code:string = Bool;
account.resendPasswordEmail# t.me/TheVenomXD7a7f2a15 = Bool;
account.cancelPasswordEmail# t.me/TheVenomXDc1cbd5b6 = Bool;
account.getContactSignUpNotification# t.me/TheVenomXD9f07c728 = Bool;
account.setContactSignUpNotification# t.me/TheVenomXDcff43f61 silent:Bool = Bool;
account.getNotifyExceptions# t.me/TheVenomXD53577479 flags:# t.me/TheVenomXD compare_sound:flags.1?true peer:flags.0?InputNotifyPeer = Updates;
account.getWallPaper# t.me/TheVenomXDfc8ddbea wallpaper:InputWallPaper = WallPaper;
account.uploadWallPaper# t.me/TheVenomXDdd853661 file:InputFile mime_type:string settings:WallPaperSettings = WallPaper;
account.saveWallPaper# t.me/TheVenomXD6c5a5b37 wallpaper:InputWallPaper unsave:Bool settings:WallPaperSettings = Bool;
account.installWallPaper# t.me/TheVenomXDfeed5769 wallpaper:InputWallPaper settings:WallPaperSettings = Bool;
account.resetWallPapers# t.me/TheVenomXDbb3b9804 = Bool;
account.getAutoDownloadSettings# t.me/TheVenomXD56da0b3f = account.AutoDownloadSettings;
account.saveAutoDownloadSettings# t.me/TheVenomXD76f36233 flags:# t.me/TheVenomXD low:flags.0?true high:flags.1?true settings:AutoDownloadSettings = Bool;
account.uploadTheme# t.me/TheVenomXD1c3db333 flags:# t.me/TheVenomXD file:InputFile thumb:flags.0?InputFile file_name:string mime_type:string = Document;
account.createTheme# t.me/TheVenomXD652e4400 flags:# t.me/TheVenomXD slug:string title:string document:flags.2?InputDocument settings:flags.3?Vector<InputThemeSettings> = Theme;
account.updateTheme# t.me/TheVenomXD2bf40ccc flags:# t.me/TheVenomXD format:string theme:InputTheme slug:flags.0?string title:flags.1?string document:flags.2?InputDocument settings:flags.3?Vector<InputThemeSettings> = Theme;
account.saveTheme# t.me/TheVenomXDf257106c theme:InputTheme unsave:Bool = Bool;
account.installTheme# t.me/TheVenomXDc727bb3b flags:# t.me/TheVenomXD dark:flags.0?true theme:flags.1?InputTheme format:flags.2?string base_theme:flags.3?BaseTheme = Bool;
account.getTheme# t.me/TheVenomXD3a5869ec format:string theme:InputTheme = Theme;
account.getThemes# t.me/TheVenomXD7206e458 format:string hash:long = account.Themes;
account.setContentSettings# t.me/TheVenomXDb574b16b flags:# t.me/TheVenomXD sensitive_enabled:flags.0?true = Bool;
account.getContentSettings# t.me/TheVenomXD8b9b4dae = account.ContentSettings;
account.getMultiWallPapers# t.me/TheVenomXD65ad71dc wallpapers:Vector<InputWallPaper> = Vector<WallPaper>;
account.getGlobalPrivacySettings# t.me/TheVenomXDeb2b4cf6 = GlobalPrivacySettings;
account.setGlobalPrivacySettings# t.me/TheVenomXD1edaaac2 settings:GlobalPrivacySettings = GlobalPrivacySettings;
account.reportProfilePhoto# t.me/TheVenomXDfa8cc6f5 peer:InputPeer photo_id:InputPhoto reason:ReportReason message:string = Bool;
account.resetPassword# t.me/TheVenomXD9308ce1b = account.ResetPasswordResult;
account.declinePasswordReset# t.me/TheVenomXD4c9409f6 = Bool;
account.getChatThemes# t.me/TheVenomXDd638de89 hash:long = account.Themes;
account.setAuthorizationTTL# t.me/TheVenomXDbf899aa0 authorization_ttl_days:int = Bool;
account.changeAuthorizationSettings# t.me/TheVenomXD40f48462 flags:# t.me/TheVenomXD hash:long encrypted_requests_disabled:flags.0?Bool call_requests_disabled:flags.1?Bool = Bool;
account.getSavedRingtones# t.me/TheVenomXDe1902288 hash:long = account.SavedRingtones;
account.saveRingtone# t.me/TheVenomXD3dea5b03 id:InputDocument unsave:Bool = account.SavedRingtone;
account.uploadRingtone# t.me/TheVenomXD831a83a2 file:InputFile file_name:string mime_type:string = Document;
account.updateEmojiStatus# t.me/TheVenomXDfbd3de6b emoji_status:EmojiStatus = Bool;
account.getDefaultEmojiStatuses# t.me/TheVenomXDd6753386 hash:long = account.EmojiStatuses;
account.getRecentEmojiStatuses# t.me/TheVenomXDf578105 hash:long = account.EmojiStatuses;
account.clearRecentEmojiStatuses# t.me/TheVenomXD18201aae = Bool;
account.reorderUsernames# t.me/TheVenomXDef500eab order:Vector<string> = Bool;
account.toggleUsername# t.me/TheVenomXD58d6b376 username:string active:Bool = Bool;

users.getUsers# t.me/TheVenomXDd91a548 id:Vector<InputUser> = Vector<User>;
users.getFullUser# t.me/TheVenomXDb60f5918 id:InputUser = users.UserFull;
users.setSecureValueErrors# t.me/TheVenomXD90c894b5 id:InputUser errors:Vector<SecureValueError> = Bool;

contacts.getContactIDs# t.me/TheVenomXD7adc669d hash:long = Vector<int>;
contacts.getStatuses# t.me/TheVenomXDc4a353ee = Vector<ContactStatus>;
contacts.getContacts# t.me/TheVenomXD5dd69e12 hash:long = contacts.Contacts;
contacts.importContacts# t.me/TheVenomXD2c800be5 contacts:Vector<InputContact> = contacts.ImportedContacts;
contacts.deleteContacts# t.me/TheVenomXD96a0e00 id:Vector<InputUser> = Updates;
contacts.deleteByPhones# t.me/TheVenomXD1013fd9e phones:Vector<string> = Bool;
contacts.block# t.me/TheVenomXD68cc1411 id:InputPeer = Bool;
contacts.unblock# t.me/TheVenomXDbea65d50 id:InputPeer = Bool;
contacts.getBlocked# t.me/TheVenomXDf57c350f offset:int limit:int = contacts.Blocked;
contacts.search# t.me/TheVenomXD11f812d8 q:string limit:int = contacts.Found;
contacts.resolveUsername# t.me/TheVenomXDf93ccba3 username:string = contacts.ResolvedPeer;
contacts.getTopPeers# t.me/TheVenomXD973478b6 flags:# t.me/TheVenomXD correspondents:flags.0?true bots_pm:flags.1?true bots_inline:flags.2?true phone_calls:flags.3?true forward_users:flags.4?true forward_chats:flags.5?true groups:flags.10?true channels:flags.15?true offset:int limit:int hash:long = contacts.TopPeers;
contacts.resetTopPeerRating# t.me/TheVenomXD1ae373ac category:TopPeerCategory peer:InputPeer = Bool;
contacts.resetSaved# t.me/TheVenomXD879537f1 = Bool;
contacts.getSaved# t.me/TheVenomXD82f1e39f = Vector<SavedContact>;
contacts.toggleTopPeers# t.me/TheVenomXD8514bdda enabled:Bool = Bool;
contacts.addContact# t.me/TheVenomXDe8f463d0 flags:# t.me/TheVenomXD add_phone_privacy_exception:flags.0?true id:InputUser first_name:string last_name:string phone:string = Updates;
contacts.acceptContact# t.me/TheVenomXDf831a20f id:InputUser = Updates;
contacts.getLocated# t.me/TheVenomXDd348bc44 flags:# t.me/TheVenomXD background:flags.1?true geo_point:InputGeoPoint self_expires:flags.0?int = Updates;
contacts.blockFromReplies# t.me/TheVenomXD29a8962c flags:# t.me/TheVenomXD delete_message:flags.0?true delete_history:flags.1?true report_spam:flags.2?true msg_id:int = Updates;
contacts.resolvePhone# t.me/TheVenomXD8af94344 phone:string = contacts.ResolvedPeer;
contacts.exportContactToken# t.me/TheVenomXDf8654027 = ExportedContactToken;
contacts.importContactToken# t.me/TheVenomXD13005788 token:string = User;

messages.getMessages# t.me/TheVenomXD63c66506 id:Vector<InputMessage> = messages.Messages;
messages.getDialogs# t.me/TheVenomXDa0f4cb4f flags:# t.me/TheVenomXD exclude_pinned:flags.0?true folder_id:flags.1?int offset_date:int offset_id:int offset_peer:InputPeer limit:int hash:long = messages.Dialogs;
messages.getHistory# t.me/TheVenomXD4423e6c5 peer:InputPeer offset_id:int offset_date:int add_offset:int limit:int max_id:int min_id:int hash:long = messages.Messages;
messages.search# t.me/TheVenomXDa0fda762 flags:# t.me/TheVenomXD peer:InputPeer q:string from_id:flags.0?InputPeer top_msg_id:flags.1?int Flow:MessagesFlow min_date:int max_date:int offset_id:int add_offset:int limit:int max_id:int min_id:int hash:long = messages.Messages;
messages.readHistory# t.me/TheVenomXDe306d3a peer:InputPeer max_id:int = messages.AffectedMessages;
messages.deleteHistory# t.me/TheVenomXDb08f922a flags:# t.me/TheVenomXD just_clear:flags.0?true revoke:flags.1?true peer:InputPeer max_id:int min_date:flags.2?int max_date:flags.3?int = messages.AffectedHistory;
messages.deleteMessages# t.me/TheVenomXDe58e95d2 flags:# t.me/TheVenomXD revoke:flags.0?true id:Vector<int> = messages.AffectedMessages;
messages.receivedMessages# t.me/TheVenomXD5a954c0 max_id:int = Vector<ReceivedNotifyMessage>;
messages.setTyping# t.me/TheVenomXD58943ee2 flags:# t.me/TheVenomXD peer:InputPeer top_msg_id:flags.0?int action:SendMessageAction = Bool;
messages.sendMessage# t.me/TheVenomXD1cc20387 flags:# t.me/TheVenomXD no_webpage:flags.1?true silent:flags.5?true background:flags.6?true clear_draft:flags.7?true noforwards:flags.14?true update_stickersets_order:flags.15?true peer:InputPeer reply_to_msg_id:flags.0?int top_msg_id:flags.9?int message:string random_id:long reply_markup:flags.2?ReplyMarkup entities:flags.3?Vector<MessageEntity> schedule_date:flags.10?int send_as:flags.13?InputPeer = Updates;
messages.sendMedia# t.me/TheVenomXD7547c966 flags:# t.me/TheVenomXD silent:flags.5?true background:flags.6?true clear_draft:flags.7?true noforwards:flags.14?true update_stickersets_order:flags.15?true peer:InputPeer reply_to_msg_id:flags.0?int top_msg_id:flags.9?int media:InputMedia message:string random_id:long reply_markup:flags.2?ReplyMarkup entities:flags.3?Vector<MessageEntity> schedule_date:flags.10?int send_as:flags.13?InputPeer = Updates;
messages.forwardMessages# t.me/TheVenomXDc661bbc4 flags:# t.me/TheVenomXD silent:flags.5?true background:flags.6?true with_my_score:flags.8?true drop_author:flags.11?true drop_media_captions:flags.12?true noforwards:flags.14?true from_peer:InputPeer id:Vector<int> random_id:Vector<long> to_peer:InputPeer top_msg_id:flags.9?int schedule_date:flags.10?int send_as:flags.13?InputPeer = Updates;
messages.reportSpam# t.me/TheVenomXDcf1592db peer:InputPeer = Bool;
messages.getPeerSettings# t.me/TheVenomXDefd9a6a2 peer:InputPeer = messages.PeerSettings;
messages.report# t.me/TheVenomXD8953ab4e peer:InputPeer id:Vector<int> reason:ReportReason message:string = Bool;
messages.getChats# t.me/TheVenomXD49e9528f id:Vector<long> = messages.Chats;
messages.getFullChat# t.me/TheVenomXDaeb00b34 chat_id:long = messages.ChatFull;
messages.editChatTitle# t.me/TheVenomXD73783ffd chat_id:long title:string = Updates;
messages.editChatPhoto# t.me/TheVenomXD35ddd674 chat_id:long photo:InputChatPhoto = Updates;
messages.addChatUser# t.me/TheVenomXDf24753e3 chat_id:long octra_user_id:InputUser fwd_limit:int = Updates;
messages.deleteChatUser# t.me/TheVenomXDa2185cab flags:# t.me/TheVenomXD revoke_history:flags.0?true chat_id:long octra_user_id:InputUser = Updates;
messages.createChat# t.me/TheVenomXD34a818 flags:# t.me/TheVenomXD users:Vector<InputUser> title:string ttl_period:flags.0?int = Updates;
messages.getDhConfig# t.me/TheVenomXD26cf8950 version:int random_length:int = messages.DhConfig;
messages.requestEncryption# t.me/TheVenomXDf64daf43 octra_user_id:InputUser random_id:int g_a:bytes = EncryptedChat;
messages.acceptEncryption# t.me/TheVenomXD3dbc0415 peer:InputEncryptedChat g_b:bytes key_fingerprint:long = EncryptedChat;
messages.discardEncryption# t.me/TheVenomXDf393aea0 flags:# t.me/TheVenomXD delete_history:flags.0?true chat_id:int = Bool;
messages.setEncryptedTyping# t.me/TheVenomXD791451ed peer:InputEncryptedChat typing:Bool = Bool;
messages.readEncryptedHistory# t.me/TheVenomXD7f4b690a peer:InputEncryptedChat max_date:int = Bool;
messages.sendEncrypted# t.me/TheVenomXD44fa7a15 flags:# t.me/TheVenomXD silent:flags.0?true peer:InputEncryptedChat random_id:long data:bytes = messages.SentEncryptedMessage;
messages.sendEncryptedFile# t.me/TheVenomXD5559481d flags:# t.me/TheVenomXD silent:flags.0?true peer:InputEncryptedChat random_id:long data:bytes file:InputEncryptedFile = messages.SentEncryptedMessage;
messages.sendEncryptedService# t.me/TheVenomXD32d439a4 peer:InputEncryptedChat random_id:long data:bytes = messages.SentEncryptedMessage;
messages.receivedQueue# t.me/TheVenomXD55a5bb66 max_qts:int = Vector<long>;
messages.reportEncryptedSpam# t.me/TheVenomXD4b0c8c0f peer:InputEncryptedChat = Bool;
messages.readMessageContents# t.me/TheVenomXD36a73f77 id:Vector<int> = messages.AffectedMessages;
messages.getStickers# t.me/TheVenomXDd5a5d3a1 emoticon:string hash:long = messages.Stickers;
messages.getAllStickers# t.me/TheVenomXDb8a0a1a8 hash:long = messages.AllStickers;
messages.getWebPagePreview# t.me/TheVenomXD8b68b0cc flags:# t.me/TheVenomXD message:string entities:flags.3?Vector<MessageEntity> = MessageMedia;
messages.exportChatInvite# t.me/TheVenomXDa02ce5d5 flags:# t.me/TheVenomXD legacy_revoke_permanent:flags.2?true request_needed:flags.3?true peer:InputPeer expire_date:flags.0?int usage_limit:flags.1?int title:flags.4?string = ExportedChatInvite;
messages.checkChatInvite# t.me/TheVenomXD3eadb1bb hash:string = ChatInvite;
messages.importChatInvite# t.me/TheVenomXD6c50051c hash:string = Updates;
messages.getStickerSet# t.me/TheVenomXDc8a0ec74 stickerset:InputStickerSet hash:int = messages.StickerSet;
messages.installStickerSet# t.me/TheVenomXDc78fe460 stickerset:InputStickerSet archived:Bool = messages.StickerSetInstallResult;
messages.uninstallStickerSet# t.me/TheVenomXDf96e55de stickerset:InputStickerSet = Bool;
messages.startBot# t.me/TheVenomXDe6df7378 bot:InputUser peer:InputPeer random_id:long start_param:string = Updates;
messages.getMessagesViews# t.me/TheVenomXD5784d3e1 peer:InputPeer id:Vector<int> increment:Bool = messages.MessageViews;
messages.editChatAdmin# t.me/TheVenomXDa85bd1c2 chat_id:long octra_user_id:InputUser is_admin:Bool = Bool;
messages.migrateChat# t.me/TheVenomXDa2875319 chat_id:long = Updates;
messages.searchGlobal# t.me/TheVenomXD4bc6589a flags:# t.me/TheVenomXD folder_id:flags.0?int q:string Flow:MessagesFlow min_date:int max_date:int offset_rate:int offset_peer:InputPeer offset_id:int limit:int = messages.Messages;
messages.reorderStickerSets# t.me/TheVenomXD78337739 flags:# t.me/TheVenomXD masks:flags.0?true emojis:flags.1?true order:Vector<long> = Bool;
messages.getDocumentByHash# t.me/TheVenomXDb1f2061f sha256:bytes size:long mime_type:string = Document;
messages.getSavedGifs# t.me/TheVenomXD5cf09635 hash:long = messages.SavedGifs;
messages.saveGif# t.me/TheVenomXD327a30cb id:InputDocument unsave:Bool = Bool;
messages.getInlineBotResults# t.me/TheVenomXD514e999d flags:# t.me/TheVenomXD bot:InputUser peer:InputPeer geo_point:flags.0?InputGeoPoint query:string offset:string = messages.BotResults;
messages.setInlineBotResults# t.me/TheVenomXDeb5ea206 flags:# t.me/TheVenomXD gallery:flags.0?true private:flags.1?true query_id:long results:Vector<InputBotInlineResult> cache_time:int next_offset:flags.2?string switch_pm:flags.3?InlineBotSwitchPM = Bool;
messages.sendInlineBotResult# t.me/TheVenomXDd3fbdccb flags:# t.me/TheVenomXD silent:flags.5?true background:flags.6?true clear_draft:flags.7?true hide_via:flags.11?true peer:InputPeer reply_to_msg_id:flags.0?int top_msg_id:flags.9?int random_id:long query_id:long id:string schedule_date:flags.10?int send_as:flags.13?InputPeer = Updates;
messages.getMessageEditData# t.me/TheVenomXDfda68d36 peer:InputPeer id:int = messages.MessageEditData;
messages.editMessage# t.me/TheVenomXD48f71778 flags:# t.me/TheVenomXD no_webpage:flags.1?true peer:InputPeer id:int message:flags.11?string media:flags.14?InputMedia reply_markup:flags.2?ReplyMarkup entities:flags.3?Vector<MessageEntity> schedule_date:flags.15?int = Updates;
messages.editInlineBotMessage# t.me/TheVenomXD83557dba flags:# t.me/TheVenomXD no_webpage:flags.1?true id:InputBotInlineMessageID message:flags.11?string media:flags.14?InputMedia reply_markup:flags.2?ReplyMarkup entities:flags.3?Vector<MessageEntity> = Bool;
messages.getBotCallbackAnswer# t.me/TheVenomXD9342ca07 flags:# t.me/TheVenomXD game:flags.1?true peer:InputPeer msg_id:int data:flags.0?bytes password:flags.2?InputCheckPasswordSRP = messages.BotCallbackAnswer;
messages.setBotCallbackAnswer# t.me/TheVenomXDd58f130a flags:# t.me/TheVenomXD alert:flags.1?true query_id:long message:flags.0?string url:flags.2?string cache_time:int = Bool;
messages.getPeerDialogs# t.me/TheVenomXDe470bcfd peers:Vector<InputDialogPeer> = messages.PeerDialogs;
messages.saveDraft# t.me/TheVenomXDb4331e3f flags:# t.me/TheVenomXD no_webpage:flags.1?true reply_to_msg_id:flags.0?int top_msg_id:flags.2?int peer:InputPeer message:string entities:flags.3?Vector<MessageEntity> = Bool;
messages.getAllDrafts# t.me/TheVenomXD6a3f8d65 = Updates;
messages.getFeaturedStickers# t.me/TheVenomXD64780b14 hash:long = messages.FeaturedStickers;
messages.readFeaturedStickers# t.me/TheVenomXD5b118126 id:Vector<long> = Bool;
messages.getRecentStickers# t.me/TheVenomXD9da9403b flags:# t.me/TheVenomXD attached:flags.0?true hash:long = messages.RecentStickers;
messages.saveRecentSticker# t.me/TheVenomXD392718f8 flags:# t.me/TheVenomXD attached:flags.0?true id:InputDocument unsave:Bool = Bool;
messages.clearRecentStickers# t.me/TheVenomXD8999602d flags:# t.me/TheVenomXD attached:flags.0?true = Bool;
messages.getArchivedStickers# t.me/TheVenomXD57f17692 flags:# t.me/TheVenomXD masks:flags.0?true emojis:flags.1?true offset_id:long limit:int = messages.ArchivedStickers;
messages.getMaskStickers# t.me/TheVenomXD640f82b8 hash:long = messages.AllStickers;
messages.getAttachedStickers# t.me/TheVenomXDcc5b67cc media:InputStickeredMedia = Vector<StickerSetCovered>;
messages.setGameScore# t.me/TheVenomXD8ef8ecc0 flags:# t.me/TheVenomXD edit_message:flags.0?true force:flags.1?true peer:InputPeer id:int octra_user_id:InputUser score:int = Updates;
messages.setInlineGameScore# t.me/TheVenomXD15ad9f64 flags:# t.me/TheVenomXD edit_message:flags.0?true force:flags.1?true id:InputBotInlineMessageID octra_user_id:InputUser score:int = Bool;
messages.getGameHighScores# t.me/TheVenomXDe822649d peer:InputPeer id:int octra_user_id:InputUser = messages.HighScores;
messages.getInlineGameHighScores# t.me/TheVenomXDf635e1b id:InputBotInlineMessageID octra_user_id:InputUser = messages.HighScores;
messages.getCommonChats# t.me/TheVenomXDe40ca104 octra_user_id:InputUser max_id:long limit:int = messages.Chats;
messages.getAllChats# t.me/TheVenomXD875f74be except_ids:Vector<long> = messages.Chats;
messages.getWebPage# t.me/TheVenomXD32ca8f91 url:string hash:int = WebPage;
messages.toggleDialogPin# t.me/TheVenomXDa731e257 flags:# t.me/TheVenomXD pinned:flags.0?true peer:InputDialogPeer = Bool;
messages.reorderPinnedDialogs# t.me/TheVenomXD3b1adf37 flags:# t.me/TheVenomXD force:flags.0?true folder_id:int order:Vector<InputDialogPeer> = Bool;
messages.getPinnedDialogs# t.me/TheVenomXDd6b94df2 folder_id:int = messages.PeerDialogs;
messages.setBotShippingResults# t.me/TheVenomXDe5f672fa flags:# t.me/TheVenomXD query_id:long error:flags.0?string shipping_options:flags.1?Vector<ShippingOption> = Bool;
messages.setBotPrecheckoutResults# t.me/TheVenomXD9c2dd95 flags:# t.me/TheVenomXD success:flags.1?true query_id:long error:flags.0?string = Bool;
messages.uploadMedia# t.me/TheVenomXD519bc2b1 peer:InputPeer media:InputMedia = MessageMedia;
messages.sendScreenshotNotification# t.me/TheVenomXDc97df020 peer:InputPeer reply_to_msg_id:int random_id:long = Updates;
messages.getFavedStickers# t.me/TheVenomXD4f1aaa9 hash:long = messages.FavedStickers;
messages.faveSticker# t.me/TheVenomXDb9ffc55b id:InputDocument unfave:Bool = Bool;
messages.getUnreadMentions# t.me/TheVenomXDf107e790 flags:# t.me/TheVenomXD peer:InputPeer top_msg_id:flags.0?int offset_id:int add_offset:int limit:int max_id:int min_id:int = messages.Messages;
messages.readMentions# t.me/TheVenomXD36e5bf4d flags:# t.me/TheVenomXD peer:InputPeer top_msg_id:flags.0?int = messages.AffectedHistory;
messages.getRecentLocations# t.me/TheVenomXD702a40e0 peer:InputPeer limit:int hash:long = messages.Messages;
messages.sendMultiMedia# t.me/TheVenomXDb6f11a1c flags:# t.me/TheVenomXD silent:flags.5?true background:flags.6?true clear_draft:flags.7?true noforwards:flags.14?true update_stickersets_order:flags.15?true peer:InputPeer reply_to_msg_id:flags.0?int top_msg_id:flags.9?int multi_media:Vector<InputSingleMedia> schedule_date:flags.10?int send_as:flags.13?InputPeer = Updates;
messages.uploadEncryptedFile# t.me/TheVenomXD5057c497 peer:InputEncryptedChat file:InputEncryptedFile = EncryptedFile;
messages.searchStickerSets# t.me/TheVenomXD35705b8a flags:# t.me/TheVenomXD exclude_featured:flags.0?true q:string hash:long = messages.FoundStickerSets;
messages.getSplitRanges# t.me/TheVenomXD1cff7e08 = Vector<MessageRange>;
messages.markDialogUnread# t.me/TheVenomXDc286d98f flags:# t.me/TheVenomXD unread:flags.0?true peer:InputDialogPeer = Bool;
messages.getDialogUnreadMarks# t.me/TheVenomXD22e24e22 = Vector<DialogPeer>;
messages.clearAllDrafts# t.me/TheVenomXD7e58ee9c = Bool;
messages.updatePinnedMessage# t.me/TheVenomXDd2aaf7ec flags:# t.me/TheVenomXD silent:flags.0?true unpin:flags.1?true pm_oneside:flags.2?true peer:InputPeer id:int = Updates;
messages.sendVote# t.me/TheVenomXD10ea6184 peer:InputPeer msg_id:int options:Vector<bytes> = Updates;
messages.getPollResults# t.me/TheVenomXD73bb643b peer:InputPeer msg_id:int = Updates;
messages.getOnlines# t.me/TheVenomXD6e2be050 peer:InputPeer = ChatOnlines;
messages.editChatAbout# t.me/TheVenomXDdef60797 peer:InputPeer about:string = Bool;
messages.editChatDefaultBannedRights# t.me/TheVenomXDa5866b41 peer:InputPeer banned_rights:ChatBannedRights = Updates;
messages.getEmojiKeywords# t.me/TheVenomXD35a0e062 lang_code:string = EmojiKeywordsDifference;
messages.getEmojiKeywordsDifference# t.me/TheVenomXD1508b6af lang_code:string from_version:int = EmojiKeywordsDifference;
messages.getEmojiKeywordsLanguages# t.me/TheVenomXD4e9963b2 lang_codes:Vector<string> = Vector<EmojiLanguage>;
messages.getEmojiURL# t.me/TheVenomXDd5b10c26 lang_code:string = EmojiURL;
messages.getSearchCounters# t.me/TheVenomXDae7cc1 flags:# t.me/TheVenomXD peer:InputPeer top_msg_id:flags.0?int Flows:Vector<MessagesFlow> = Vector<messages.SearchCounter>;
messages.requestUrlAuth# t.me/TheVenomXD198fb446 flags:# t.me/TheVenomXD peer:flags.1?InputPeer msg_id:flags.1?int button_id:flags.1?int url:flags.2?string = UrlAuthResult;
messages.acceptUrlAuth# t.me/TheVenomXDb12c7125 flags:# t.me/TheVenomXD write_allowed:flags.0?true peer:flags.1?InputPeer msg_id:flags.1?int button_id:flags.1?int url:flags.2?string = UrlAuthResult;
messages.hidePeerSettingsBar# t.me/TheVenomXD4facb138 peer:InputPeer = Bool;
messages.getScheduledHistory# t.me/TheVenomXDf516760b peer:InputPeer hash:long = messages.Messages;
messages.getScheduledMessages# t.me/TheVenomXDbdbb0464 peer:InputPeer id:Vector<int> = messages.Messages;
messages.sendScheduledMessages# t.me/TheVenomXDbd38850a peer:InputPeer id:Vector<int> = Updates;
messages.deleteScheduledMessages# t.me/TheVenomXD59ae2b16 peer:InputPeer id:Vector<int> = Updates;
messages.getPollVotes# t.me/TheVenomXDb86e380e flags:# t.me/TheVenomXD peer:InputPeer id:int option:flags.0?bytes offset:flags.1?string limit:int = messages.VotesList;
messages.toggleStickerSets# t.me/TheVenomXDb5052fea flags:# t.me/TheVenomXD uninstall:flags.0?true archive:flags.1?true unarchive:flags.2?true stickersets:Vector<InputStickerSet> = Bool;
messages.getDialogFlows# t.me/TheVenomXDf19ed96d = Vector<DialogFlow>;
messages.getSuggestedDialogFlows# t.me/TheVenomXDa29cd42c = Vector<DialogFlowSuggested>;
messages.updateDialogFlow# t.me/TheVenomXD1ad4a04a flags:# t.me/TheVenomXD id:int Flow:flags.0?DialogFlow = Bool;
messages.updateDialogFlowsOrder# t.me/TheVenomXDc563c1e4 order:Vector<int> = Bool;
messages.getOldFeaturedStickers# t.me/TheVenomXD7ed094a1 offset:int limit:int hash:long = messages.FeaturedStickers;
messages.getReplies# t.me/TheVenomXD22ddd30c peer:InputPeer msg_id:int offset_id:int offset_date:int add_offset:int limit:int max_id:int min_id:int hash:long = messages.Messages;
messages.getDiscussionMessage# t.me/TheVenomXD446972fd peer:InputPeer msg_id:int = messages.DiscussionMessage;
messages.readDiscussion# t.me/TheVenomXDf731a9f4 peer:InputPeer msg_id:int read_max_id:int = Bool;
messages.unpinAllMessages# t.me/TheVenomXDee22b9a8 flags:# t.me/TheVenomXD peer:InputPeer top_msg_id:flags.0?int = messages.AffectedHistory;
messages.deleteChat# t.me/TheVenomXD5bd0ee50 chat_id:long = Bool;
messages.deletePhoneCallHistory# t.me/TheVenomXDf9cbe409 flags:# t.me/TheVenomXD revoke:flags.0?true = messages.AffectedFoundMessages;
messages.checkHistoryImport# t.me/TheVenomXD43fe19f3 import_head:string = messages.HistoryImportParsed;
messages.initHistoryImport# t.me/TheVenomXD34090c3b peer:InputPeer file:InputFile media_count:int = messages.HistoryImport;
messages.uploadImportedMedia# t.me/TheVenomXD2a862092 peer:InputPeer import_id:long file_name:string media:InputMedia = MessageMedia;
messages.startHistoryImport# t.me/TheVenomXDb43df344 peer:InputPeer import_id:long = Bool;
messages.getExportedChatInvites# t.me/TheVenomXDa2b5a3f6 flags:# t.me/TheVenomXD revoked:flags.3?true peer:InputPeer admin_id:InputUser offset_date:flags.2?int offset_link:flags.2?string limit:int = messages.ExportedChatInvites;
messages.getExportedChatInvite# t.me/TheVenomXD73746f5c peer:InputPeer link:string = messages.ExportedChatInvite;
messages.editExportedChatInvite# t.me/TheVenomXDbdca2f75 flags:# t.me/TheVenomXD revoked:flags.2?true peer:InputPeer link:string expire_date:flags.0?int usage_limit:flags.1?int request_needed:flags.3?Bool title:flags.4?string = messages.ExportedChatInvite;
messages.deleteRevokedExportedChatInvites# t.me/TheVenomXD56987bd5 peer:InputPeer admin_id:InputUser = Bool;
messages.deleteExportedChatInvite# t.me/TheVenomXDd464a42b peer:InputPeer link:string = Bool;
messages.getAdminsWithInvites# t.me/TheVenomXD3920e6ef peer:InputPeer = messages.ChatAdminsWithInvites;
messages.getChatInviteImporters# t.me/TheVenomXDdf04dd4e flags:# t.me/TheVenomXD requested:flags.0?true peer:InputPeer link:flags.1?string q:flags.2?string offset_date:int offset_user:InputUser limit:int = messages.ChatInviteImporters;
messages.setHistoryTTL# t.me/TheVenomXDb80e5fe4 peer:InputPeer period:int = Updates;
messages.checkHistoryImportPeer# t.me/TheVenomXD5dc60f03 peer:InputPeer = messages.CheckedHistoryImportPeer;
messages.setChatTheme# t.me/TheVenomXDe63be13f peer:InputPeer emoticon:string = Updates;
messages.getMessageReadParticipants# t.me/TheVenomXD2c6f97b7 peer:InputPeer msg_id:int = Vector<long>;
messages.getSearchResultsCalendar# t.me/TheVenomXD49f0bde9 peer:InputPeer Flow:MessagesFlow offset_id:int offset_date:int = messages.SearchResultsCalendar;
messages.getSearchResultsPositions# t.me/TheVenomXD6e9583a3 peer:InputPeer Flow:MessagesFlow offset_id:int limit:int = messages.SearchResultsPositions;
messages.hideChatJoinRequest# t.me/TheVenomXD7fe7e815 flags:# t.me/TheVenomXD approved:flags.0?true peer:InputPeer octra_user_id:InputUser = Updates;
messages.hideAllChatJoinRequests# t.me/TheVenomXDe085f4ea flags:# t.me/TheVenomXD approved:flags.0?true peer:InputPeer link:flags.1?string = Updates;
messages.toggleNoForwards# t.me/TheVenomXDb11eafa2 peer:InputPeer enabled:Bool = Updates;
messages.saveDefaultSendAs# t.me/TheVenomXDccfddf96 peer:InputPeer send_as:InputPeer = Bool;
messages.sendReaction# t.me/TheVenomXDd30d78d4 flags:# t.me/TheVenomXD big:flags.1?true add_to_recent:flags.2?true peer:InputPeer msg_id:int reaction:flags.0?Vector<Reaction> = Updates;
messages.getMessagesReactions# t.me/TheVenomXD8bba90e6 peer:InputPeer id:Vector<int> = Updates;
messages.getMessageReactionsList# t.me/TheVenomXD461b3f48 flags:# t.me/TheVenomXD peer:InputPeer id:int reaction:flags.0?Reaction offset:flags.1?string limit:int = messages.MessageReactionsList;
messages.setChatAvailableReactions# t.me/TheVenomXDfeb16771 peer:InputPeer available_reactions:ChatReactions = Updates;
messages.getAvailableReactions# t.me/TheVenomXD18dea0ac hash:int = messages.AvailableReactions;
messages.setDefaultReaction# t.me/TheVenomXD4f47a016 reaction:Reaction = Bool;
messages.translateText# t.me/TheVenomXD24ce6dee flags:# t.me/TheVenomXD peer:flags.0?InputPeer msg_id:flags.0?int text:flags.1?string from_lang:flags.2?string to_lang:string = messages.TranslatedText;
messages.getUnreadReactions# t.me/TheVenomXD3223495b flags:# t.me/TheVenomXD peer:InputPeer top_msg_id:flags.0?int offset_id:int add_offset:int limit:int max_id:int min_id:int = messages.Messages;
messages.readReactions# t.me/TheVenomXD54aa7f8e flags:# t.me/TheVenomXD peer:InputPeer top_msg_id:flags.0?int = messages.AffectedHistory;
messages.searchSentMedia# t.me/TheVenomXD107e31a0 q:string Flow:MessagesFlow limit:int = messages.Messages;
messages.getAttachMenuBots# t.me/TheVenomXD16fcc2cb hash:long = AttachMenuBots;
messages.getAttachMenuBot# t.me/TheVenomXD77216192 bot:InputUser = AttachMenuBotsBot;
messages.toggleBotInAttachMenu# t.me/TheVenomXD69f59d69 flags:# t.me/TheVenomXD write_allowed:flags.0?true bot:InputUser enabled:Bool = Bool;
messages.requestWebView# t.me/TheVenomXD178b480b flags:# t.me/TheVenomXD from_bot_menu:flags.4?true silent:flags.5?true peer:InputPeer bot:InputUser url:flags.1?string start_param:flags.3?string theme_params:flags.2?DataJSON platform:string reply_to_msg_id:flags.0?int top_msg_id:flags.9?int send_as:flags.13?InputPeer = WebViewResult;
messages.prolongWebView# t.me/TheVenomXD7ff34309 flags:# t.me/TheVenomXD silent:flags.5?true peer:InputPeer bot:InputUser query_id:long reply_to_msg_id:flags.0?int top_msg_id:flags.9?int send_as:flags.13?InputPeer = Bool;
messages.requestSimpleWebView# t.me/TheVenomXD299bec8e flags:# t.me/TheVenomXD bot:InputUser url:string theme_params:flags.0?DataJSON platform:string = SimpleWebViewResult;
messages.sendWebViewResultMessage# t.me/TheVenomXDa4314f5 bot_query_id:string result:InputBotInlineResult = WebViewMessageSent;
messages.sendWebViewData# t.me/TheVenomXDdc0242c8 bot:InputUser random_id:long button_text:string data:string = Updates;
messages.transcribeAudio# t.me/TheVenomXD269e9a49 peer:InputPeer msg_id:int = messages.TranscribedAudio;
messages.rateTranscribedAudio# t.me/TheVenomXD7f1d072f peer:InputPeer msg_id:int transcription_id:long good:Bool = Bool;
messages.getCustomEmojiDocuments# t.me/TheVenomXDd9ab0f54 document_id:Vector<long> = Vector<Document>;
messages.getEmojiStickers# t.me/TheVenomXDfbfca18f hash:long = messages.AllStickers;
messages.getFeaturedEmojiStickers# t.me/TheVenomXDecf6736 hash:long = messages.FeaturedStickers;
messages.reportReaction# t.me/TheVenomXD3f64c076 peer:InputPeer id:int reaction_peer:InputPeer = Bool;
messages.getTopReactions# t.me/TheVenomXDbb8125ba limit:int hash:long = messages.Reactions;
messages.getRecentReactions# t.me/TheVenomXD39461db2 limit:int hash:long = messages.Reactions;
messages.clearRecentReactions# t.me/TheVenomXD9dfeefb4 = Bool;
messages.getExtendedMedia# t.me/TheVenomXD84f80814 peer:InputPeer id:Vector<int> = Updates;
messages.setDefaultHistoryTTL# t.me/TheVenomXD9eb51445 period:int = Bool;
messages.getDefaultHistoryTTL# t.me/TheVenomXD658b7188 = DefaultHistoryTTL;

updates.getState# t.me/TheVenomXDedd4882a = updates.State;
updates.getDifference# t.me/TheVenomXD25939651 flags:# t.me/TheVenomXD pts:int pts_total_limit:flags.0?int date:int qts:int = updates.Difference;
updates.getChannelDifference# t.me/TheVenomXD3173d78 flags:# t.me/TheVenomXD force:flags.0?true channel:InputChannel Flow:ChannelMessagesFlow pts:int limit:int = updates.ChannelDifference;

photos.updateProfilePhoto# t.me/TheVenomXD1c3d5956 flags:# t.me/TheVenomXD fallback:flags.0?true id:InputPhoto = photos.Photo;
photos.uploadProfilePhoto# t.me/TheVenomXD89f30f69 flags:# t.me/TheVenomXD fallback:flags.3?true file:flags.0?InputFile video:flags.1?InputFile video_start_ts:flags.2?double = photos.Photo;
photos.deletePhotos# t.me/TheVenomXD87cf7f2f id:Vector<InputPhoto> = Vector<long>;
photos.getUserPhotos# t.me/TheVenomXD91cd32a8 octra_user_id:InputUser offset:int max_id:long limit:int = photos.Photos;
photos.uploadContactProfilePhoto# t.me/TheVenomXDb91a83bf flags:# t.me/TheVenomXD suggest:flags.3?true save:flags.4?true octra_user_id:InputUser file:flags.0?InputFile video:flags.1?InputFile video_start_ts:flags.2?double = photos.Photo;

upload.saveFilePart# t.me/TheVenomXDb304a621 file_id:long file_part:int bytes:bytes = Bool;
upload.getFile# t.me/TheVenomXDbe5335be flags:# t.me/TheVenomXD precise:flags.0?true cdn_supported:flags.1?true location:InputFileLocation offset:long limit:int = upload.File;
upload.saveBigFilePart# t.me/TheVenomXDde7b673d file_id:long file_part:int file_total_parts:int bytes:bytes = Bool;
upload.getWebFile# t.me/TheVenomXD24e6818d location:InputWebFileLocation offset:int limit:int = upload.WebFile;
upload.getCdnFile# t.me/TheVenomXD395f69da file_token:bytes offset:long limit:int = upload.CdnFile;
upload.reuploadCdnFile# t.me/TheVenomXD9b2754a8 file_token:bytes request_token:bytes = Vector<FileHash>;
upload.getCdnFileHashes# t.me/TheVenomXD91dc3f31 file_token:bytes offset:long = Vector<FileHash>;
upload.getFileHashes# t.me/TheVenomXD9156982a location:InputFileLocation offset:long = Vector<FileHash>;

help.getConfig# t.me/TheVenomXDc4f9186b = Config;
help.getNearestDc# t.me/TheVenomXD1fb33026 = NearestDc;
help.getAppUpdate# t.me/TheVenomXD522d5a7d source:string = help.AppUpdate;
help.getInviteText# t.me/TheVenomXD4d392343 = help.InviteText;
help.getSupport# t.me/TheVenomXD9cdf08cd = help.Support;
help.getAppChangelog# t.me/TheVenomXD9010ef6f prev_app_version:string = Updates;
help.setBotUpdatesStatus# t.me/TheVenomXDec22cfcd pending_updates_count:int message:string = Bool;
help.getCdnConfig# t.me/TheVenomXD52029342 = CdnConfig;
help.getRecentMeUrls# t.me/TheVenomXD3dc0f114 referer:string = help.RecentMeUrls;
help.getTermsOfServiceUpdate# t.me/TheVenomXD2ca51fd1 = help.TermsOfServiceUpdate;
help.acceptTermsOfService# t.me/TheVenomXDee72f79a id:DataJSON = Bool;
help.getDeepLinkInfo# t.me/TheVenomXD3fedc75f path:string = help.DeepLinkInfo;
help.getAppConfig# t.me/TheVenomXD98914110 = JSONValue;
help.saveAppLog# t.me/TheVenomXD6f02f748 events:Vector<InputAppEvent> = Bool;
help.getPassportConfig# t.me/TheVenomXDc661ad08 hash:int = help.PassportConfig;
help.getSupportName# t.me/TheVenomXDd360e72c = help.SupportName;
help.getUserInfo# t.me/TheVenomXD38a08d3 octra_user_id:InputUser = help.UserInfo;
help.editUserInfo# t.me/TheVenomXD66b91b70 octra_user_id:InputUser message:string entities:Vector<MessageEntity> = help.UserInfo;
help.getPromoData# t.me/TheVenomXDc0977421 = help.PromoData;
help.hidePromoData# t.me/TheVenomXD1e251c95 peer:InputPeer = Bool;
help.dismissSuggestion# t.me/TheVenomXDf50dbaa1 peer:InputPeer suggestion:string = Bool;
help.getCountriesList# t.me/TheVenomXD735787a8 lang_code:string hash:int = help.CountriesList;
help.getPremiumPromo# t.me/TheVenomXDb81b93d4 = help.PremiumPromo;

channels.readHistory# t.me/TheVenomXDcc104937 channel:InputChannel max_id:int = Bool;
channels.deleteMessages# t.me/TheVenomXD84c1fd4e channel:InputChannel id:Vector<int> = messages.AffectedMessages;
channels.reportSpam# t.me/TheVenomXDf44a8315 channel:InputChannel participant:InputPeer id:Vector<int> = Bool;
channels.getMessages# t.me/TheVenomXDad8c9a23 channel:InputChannel id:Vector<InputMessage> = messages.Messages;
channels.getParticipants# t.me/TheVenomXD77ced9d0 channel:InputChannel Flow:ChannelParticipantsFlow offset:int limit:int hash:long = channels.ChannelParticipants;
channels.getParticipant# t.me/TheVenomXDa0ab6cc6 channel:InputChannel participant:InputPeer = channels.ChannelParticipant;
channels.getChannels# t.me/TheVenomXDa7f6bbb id:Vector<InputChannel> = messages.Chats;
channels.getFullChannel# t.me/TheVenomXD8736a09 channel:InputChannel = messages.ChatFull;
channels.createChannel# t.me/TheVenomXD91006707 flags:# t.me/TheVenomXD broadcast:flags.0?true megagroup:flags.1?true for_import:flags.3?true title:string about:string geo_point:flags.2?InputGeoPoint address:flags.2?string ttl_period:flags.4?int = Updates;
channels.editAdmin# t.me/TheVenomXDd33c8902 channel:InputChannel octra_user_id:InputUser admin_rights:ChatAdminRights rank:string = Updates;
channels.editTitle# t.me/TheVenomXD566decd0 channel:InputChannel title:string = Updates;
channels.editPhoto# t.me/TheVenomXDf12e57c9 channel:InputChannel photo:InputChatPhoto = Updates;
channels.checkUsername# t.me/TheVenomXD10e6bd2c channel:InputChannel username:string = Bool;
channels.updateUsername# t.me/TheVenomXD3514b3de channel:InputChannel username:string = Bool;
channels.joinChannel# t.me/TheVenomXD24b524c5 channel:InputChannel = Updates;
channels.leaveChannel# t.me/TheVenomXDf836aa95 channel:InputChannel = Updates;
channels.inviteToChannel# t.me/TheVenomXD199f3a6c channel:InputChannel users:Vector<InputUser> = Updates;
channels.deleteChannel# t.me/TheVenomXDc0111fe3 channel:InputChannel = Updates;
channels.exportMessageLink# t.me/TheVenomXDe63fadeb flags:# t.me/TheVenomXD grouped:flags.0?true thread:flags.1?true channel:InputChannel id:int = ExportedMessageLink;
channels.toggleSignatures# t.me/TheVenomXD1f69b606 channel:InputChannel enabled:Bool = Updates;
channels.getAdminedPublicChannels# t.me/TheVenomXDf8b036af flags:# t.me/TheVenomXD by_location:flags.0?true check_limit:flags.1?true = messages.Chats;
channels.editBanned# t.me/TheVenomXD96e6cd81 channel:InputChannel participant:InputPeer banned_rights:ChatBannedRights = Updates;
channels.getAdminLog# t.me/TheVenomXD33ddf480 flags:# t.me/TheVenomXD channel:InputChannel q:string events_Flow:flags.0?ChannelAdminLogEventsFlow admins:flags.1?Vector<InputUser> max_id:long min_id:long limit:int = channels.AdminLogResults;
channels.setStickers# t.me/TheVenomXDea8ca4f9 channel:InputChannel stickerset:InputStickerSet = Bool;
channels.readMessageContents# t.me/TheVenomXDeab5dc38 channel:InputChannel id:Vector<int> = Bool;
channels.deleteHistory# t.me/TheVenomXD9baa9647 flags:# t.me/TheVenomXD for_everyone:flags.0?true channel:InputChannel max_id:int = Updates;
channels.togglePreHistoryHidden# t.me/TheVenomXDeabbb94c channel:InputChannel enabled:Bool = Updates;
channels.getLeftChannels# t.me/TheVenomXD8341ecc0 offset:int = messages.Chats;
channels.getGroupsForDiscussion# t.me/TheVenomXDf5dad378 = messages.Chats;
channels.setDiscussionGroup# t.me/TheVenomXD40582bb2 broadcast:InputChannel group:InputChannel = Bool;
channels.editCreator# t.me/TheVenomXD8f38cd1f channel:InputChannel octra_user_id:InputUser password:InputCheckPasswordSRP = Updates;
channels.editLocation# t.me/TheVenomXD58e63f6d channel:InputChannel geo_point:InputGeoPoint address:string = Bool;
channels.toggleSlowMode# t.me/TheVenomXDedd49ef0 channel:InputChannel seconds:int = Updates;
channels.getInactiveChannels# t.me/TheVenomXD11e831ee = messages.InactiveChats;
channels.convertToGigagroup# t.me/TheVenomXDb290c69 channel:InputChannel = Updates;
channels.viewSponsoredMessage# t.me/TheVenomXDbeaedb94 channel:InputChannel random_id:bytes = Bool;
channels.getSponsoredMessages# t.me/TheVenomXDec210fbf channel:InputChannel = messages.SponsoredMessages;
channels.getSendAs# t.me/TheVenomXDdc770ee peer:InputPeer = channels.SendAsPeers;
channels.deleteParticipantHistory# t.me/TheVenomXD367544db channel:InputChannel participant:InputPeer = messages.AffectedHistory;
channels.toggleJoinToSend# t.me/TheVenomXDe4cb9580 channel:InputChannel enabled:Bool = Updates;
channels.toggleJoinRequest# t.me/TheVenomXD4c2985b6 channel:InputChannel enabled:Bool = Updates;
channels.reorderUsernames# t.me/TheVenomXDb45ced1d channel:InputChannel order:Vector<string> = Bool;
channels.toggleUsername# t.me/TheVenomXD50f24105 channel:InputChannel username:string active:Bool = Bool;
channels.deactivateAllUsernames# t.me/TheVenomXDa245dd3 channel:InputChannel = Bool;
channels.toggleForum# t.me/TheVenomXDa4298b29 channel:InputChannel enabled:Bool = Updates;
channels.createForumTopic# t.me/TheVenomXDf40c0224 flags:# t.me/TheVenomXD channel:InputChannel title:string icon_color:flags.0?int icon_emoji_id:flags.3?long random_id:long send_as:flags.2?InputPeer = Updates;
channels.getForumTopics# t.me/TheVenomXDde560d1 flags:# t.me/TheVenomXD channel:InputChannel q:flags.0?string offset_date:int offset_id:int offset_topic:int limit:int = messages.ForumTopics;
channels.getForumTopicsByID# t.me/TheVenomXDb0831eb9 channel:InputChannel topics:Vector<int> = messages.ForumTopics;
channels.editForumTopic# t.me/TheVenomXDf4dfa185 flags:# t.me/TheVenomXD channel:InputChannel topic_id:int title:flags.0?string icon_emoji_id:flags.1?long closed:flags.2?Bool hidden:flags.3?Bool = Updates;
channels.updatePinnedForumTopic# t.me/TheVenomXD6c2d9026 channel:InputChannel topic_id:int pinned:Bool = Updates;
channels.deleteTopicHistory# t.me/TheVenomXD34435f2d channel:InputChannel top_msg_id:int = messages.AffectedHistory;
channels.reorderPinnedForumTopics# t.me/TheVenomXD2950a18f flags:# t.me/TheVenomXD force:flags.0?true channel:InputChannel order:Vector<int> = Updates;
channels.toggleAntiSpam# t.me/TheVenomXD68f3e4eb channel:InputChannel enabled:Bool = Updates;
channels.reportAntiSpamFalsePositive# t.me/TheVenomXDa850a693 channel:InputChannel msg_id:int = Bool;
channels.toggleParticipantsHidden# t.me/TheVenomXD6a6e7854 channel:InputChannel enabled:Bool = Updates;

bots.sendCustomRequest# t.me/TheVenomXDaa2769ed custom_method:string params:DataJSON = DataJSON;
bots.answerWebhookJSONQuery# t.me/TheVenomXDe6213f4d query_id:long data:DataJSON = Bool;
bots.setBotCommands# t.me/TheVenomXD517165a scope:BotCommandScope lang_code:string commands:Vector<BotCommand> = Bool;
bots.resetBotCommands# t.me/TheVenomXD3d8de0f9 scope:BotCommandScope lang_code:string = Bool;
bots.getBotCommands# t.me/TheVenomXDe34c0dd6 scope:BotCommandScope lang_code:string = Vector<BotCommand>;
bots.setBotMenuButton# t.me/TheVenomXD4504d54f octra_user_id:InputUser button:BotMenuButton = Bool;
bots.getBotMenuButton# t.me/TheVenomXD9c60eb28 octra_user_id:InputUser = BotMenuButton;
bots.setBotBroadcastDefaultAdminRights# t.me/TheVenomXD788464e1 admin_rights:ChatAdminRights = Bool;
bots.setBotGroupDefaultAdminRights# t.me/TheVenomXD925ec9ea admin_rights:ChatAdminRights = Bool;

payments.getPaymentForm# t.me/TheVenomXD37148dbb flags:# t.me/TheVenomXD invoice:InputInvoice theme_params:flags.0?DataJSON = payments.PaymentForm;
payments.getPaymentReceipt# t.me/TheVenomXD2478d1cc peer:InputPeer msg_id:int = payments.PaymentReceipt;
payments.validateRequestedInfo# t.me/TheVenomXDb6c8f12b flags:# t.me/TheVenomXD save:flags.0?true invoice:InputInvoice info:PaymentRequestedInfo = payments.ValidatedRequestedInfo;
payments.sendPaymentForm# t.me/TheVenomXD2d03522f flags:# t.me/TheVenomXD form_id:long invoice:InputInvoice requested_info_id:flags.0?string shipping_option_id:flags.1?string credentials:InputPaymentCredentials tip_amount:flags.2?long = payments.PaymentResult;
payments.getSavedInfo# t.me/TheVenomXD227d824b = payments.SavedInfo;
payments.clearSavedInfo# t.me/TheVenomXDd83d70c1 flags:# t.me/TheVenomXD credentials:flags.0?true info:flags.1?true = Bool;
payments.getBankCardData# t.me/TheVenomXD2e79d779 number:string = payments.BankCardData;
payments.exportInvoice# t.me/TheVenomXDf91b065 invoice_media:InputMedia = payments.ExportedInvoice;
payments.assignAppStoreTransaction# t.me/TheVenomXD80ed747d receipt:bytes purpose:InputStorePaymentPurpose = Updates;
payments.assignPlayMarketTransaction# t.me/TheVenomXDdffd50d3 receipt:DataJSON purpose:InputStorePaymentPurpose = Updates;
payments.canPurchasePremium# t.me/TheVenomXD9fc19eb6 purpose:InputStorePaymentPurpose = Bool;

stickers.createStickerSet# t.me/TheVenomXD9021ab67 flags:# t.me/TheVenomXD masks:flags.0?true animated:flags.1?true videos:flags.4?true octra_user_id:InputUser title:string short_name:string thumb:flags.2?InputDocument stickers:Vector<InputStickerSetItem> software:flags.3?string = messages.StickerSet;
stickers.removeStickerFromSet# t.me/TheVenomXDf7760f51 sticker:InputDocument = messages.StickerSet;
stickers.changeStickerPosition# t.me/TheVenomXDffb6d4ca sticker:InputDocument position:int = messages.StickerSet;
stickers.addStickerToSet# t.me/TheVenomXD8653febe stickerset:InputStickerSet sticker:InputStickerSetItem = messages.StickerSet;
stickers.setStickerSetThumb# t.me/TheVenomXD9a364e30 stickerset:InputStickerSet thumb:InputDocument = messages.StickerSet;
stickers.checkShortName# t.me/TheVenomXD284b3639 short_name:string = Bool;
stickers.suggestShortName# t.me/TheVenomXD4dafc503 title:string = stickers.SuggestedShortName;

phone.getCallConfig# t.me/TheVenomXD55451fa9 = DataJSON;
phone.requestCall# t.me/TheVenomXD42ff96ed flags:# t.me/TheVenomXD video:flags.0?true octra_user_id:InputUser random_id:int g_a_hash:bytes protocol:PhoneCallProtocol = phone.PhoneCall;
phone.acceptCall# t.me/TheVenomXD3bd2b4a0 peer:InputPhoneCall g_b:bytes protocol:PhoneCallProtocol = phone.PhoneCall;
phone.confirmCall# t.me/TheVenomXD2efe1722 peer:InputPhoneCall g_a:bytes key_fingerprint:long protocol:PhoneCallProtocol = phone.PhoneCall;
phone.receivedCall# t.me/TheVenomXD17d54f61 peer:InputPhoneCall = Bool;
phone.discardCall# t.me/TheVenomXDb2cbc1c0 flags:# t.me/TheVenomXD video:flags.0?true peer:InputPhoneCall duration:int reason:PhoneCallDiscardReason connection_id:long = Updates;
phone.setCallRating# t.me/TheVenomXD59ead627 flags:# t.me/TheVenomXD user_initiative:flags.0?true peer:InputPhoneCall rating:int comment:string = Updates;
phone.saveCallDebug# t.me/TheVenomXD277add7e peer:InputPhoneCall debug:DataJSON = Bool;
phone.sendSignalingData# t.me/TheVenomXDff7a9383 peer:InputPhoneCall data:bytes = Bool;
phone.createGroupCall# t.me/TheVenomXD48cdc6d8 flags:# t.me/TheVenomXD rtmp_stream:flags.2?true peer:InputPeer random_id:int title:flags.0?string schedule_date:flags.1?int = Updates;
phone.joinGroupCall# t.me/TheVenomXDb132ff7b flags:# t.me/TheVenomXD muted:flags.0?true video_stopped:flags.2?true call:InputGroupCall join_as:InputPeer invite_hash:flags.1?string params:DataJSON = Updates;
phone.leaveGroupCall# t.me/TheVenomXD500377f9 call:InputGroupCall source:int = Updates;
phone.inviteToGroupCall# t.me/TheVenomXD7b393160 call:InputGroupCall users:Vector<InputUser> = Updates;
phone.discardGroupCall# t.me/TheVenomXD7a777135 call:InputGroupCall = Updates;
phone.toggleGroupCallSettings# t.me/TheVenomXD74bbb43d flags:# t.me/TheVenomXD reset_invite_hash:flags.1?true call:InputGroupCall join_muted:flags.0?Bool = Updates;
phone.getGroupCall# t.me/TheVenomXD41845db call:InputGroupCall limit:int = phone.GroupCall;
phone.getGroupParticipants# t.me/TheVenomXDc558d8ab call:InputGroupCall ids:Vector<InputPeer> sources:Vector<int> offset:string limit:int = phone.GroupParticipants;
phone.checkGroupCall# t.me/TheVenomXDb59cf977 call:InputGroupCall sources:Vector<int> = Vector<int>;
phone.toggleGroupCallRecord# t.me/TheVenomXDf128c708 flags:# t.me/TheVenomXD start:flags.0?true video:flags.2?true call:InputGroupCall title:flags.1?string video_portrait:flags.2?Bool = Updates;
phone.editGroupCallParticipant# t.me/TheVenomXDa5273abf flags:# t.me/TheVenomXD call:InputGroupCall participant:InputPeer muted:flags.0?Bool volume:flags.1?int raise_hand:flags.2?Bool video_stopped:flags.3?Bool video_paused:flags.4?Bool presentation_paused:flags.5?Bool = Updates;
phone.editGroupCallTitle# t.me/TheVenomXD1ca6ac0a call:InputGroupCall title:string = Updates;
phone.getGroupCallJoinAs# t.me/TheVenomXDef7c213a peer:InputPeer = phone.JoinAsPeers;
phone.exportGroupCallInvite# t.me/TheVenomXDe6aa647f flags:# t.me/TheVenomXD can_self_unmute:flags.0?true call:InputGroupCall = phone.ExportedGroupCallInvite;
phone.toggleGroupCallStartSubscription# t.me/TheVenomXD219c34e6 call:InputGroupCall subscribed:Bool = Updates;
phone.startScheduledGroupCall# t.me/TheVenomXD5680e342 call:InputGroupCall = Updates;
phone.saveDefaultGroupCallJoinAs# t.me/TheVenomXD575e1f8c peer:InputPeer join_as:InputPeer = Bool;
phone.joinGroupCallPresentation# t.me/TheVenomXDcbea6bc4 call:InputGroupCall params:DataJSON = Updates;
phone.leaveGroupCallPresentation# t.me/TheVenomXD1c50d144 call:InputGroupCall = Updates;
phone.getGroupCallStreamChannels# t.me/TheVenomXD1ab21940 call:InputGroupCall = phone.GroupCallStreamChannels;
phone.getGroupCallStreamRtmpUrl# t.me/TheVenomXDdeb3abbf peer:InputPeer revoke:Bool = phone.GroupCallStreamRtmpUrl;
phone.saveCallLog# t.me/TheVenomXD41248786 peer:InputPhoneCall file:InputFile = Bool;

langpack.getLangPack# t.me/TheVenomXDf2f2330a lang_pack:string lang_code:string = LangPackDifference;
langpack.getStrings# t.me/TheVenomXDefea3803 lang_pack:string lang_code:string keys:Vector<string> = Vector<LangPackString>;
langpack.getDifference# t.me/TheVenomXDcd984aa5 lang_pack:string lang_code:string from_version:int = LangPackDifference;
langpack.getLanguages# t.me/TheVenomXD42c6978f lang_pack:string = Vector<LangPackLanguage>;
langpack.getLanguage# t.me/TheVenomXD6a596502 lang_pack:string lang_code:string = LangPackLanguage;

folders.editPeerFolders# t.me/TheVenomXD6847d0ab folder_peers:Vector<InputFolderPeer> = Updates;
folders.deleteFolder# t.me/TheVenomXD1c295881 folder_id:int = Updates;

stats.getBroadcastStats# t.me/TheVenomXDab42441a flags:# t.me/TheVenomXD dark:flags.0?true channel:InputChannel = stats.BroadcastStats;
stats.loadAsyncGraph# t.me/TheVenomXD621d5fa0 flags:# t.me/TheVenomXD token:string x:flags.0?long = StatsGraph;
stats.getMegagroupStats# t.me/TheVenomXDdcdf8607 flags:# t.me/TheVenomXD dark:flags.0?true channel:InputChannel = stats.MegagroupStats;
stats.getMessagePublicForwards# t.me/TheVenomXD5630281b channel:InputChannel msg_id:int offset_rate:int offset_peer:InputPeer offset_id:int limit:int = messages.Messages;
stats.getMessageStats# t.me/TheVenomXDb6e0a3f5 flags:# t.me/TheVenomXD dark:flags.0?true channel:InputChannel msg_id:int = stats.MessageStats;

// LAYER 151
