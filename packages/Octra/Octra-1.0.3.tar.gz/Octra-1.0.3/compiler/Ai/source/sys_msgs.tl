///////////////////////////////
////////////// System messages
///////////////////////////////

---types---

msgs_ack# t.me/TheVenomXD62d6b459 msg_ids:Vector<long> = MsgsAck;

bad_msg_notification# t.me/TheVenomXDa7eff811 bad_msg_id:long bad_msg_seqno:int error_code:int = BadMsgNotification;
bad_server_salt# t.me/TheVenomXDedab447b bad_msg_id:long bad_msg_seqno:int error_code:int new_server_salt:long = BadMsgNotification;

msgs_state_req# t.me/TheVenomXDda69fb52 msg_ids:Vector<long> = MsgsStateReq;
msgs_state_info# t.me/TheVenomXD04deb57d req_msg_id:long info:string = MsgsStateInfo;
msgs_all_info# t.me/TheVenomXD8cc0d131 msg_ids:Vector<long> info:string = MsgsAllInfo;

msg_detailed_info# t.me/TheVenomXD276d3ec6 msg_id:long answer_msg_id:long bytes:int status:int = MsgDetailedInfo;
msg_new_detailed_info# t.me/TheVenomXD809db6df answer_msg_id:long bytes:int status:int = MsgDetailedInfo;

msg_resend_req# t.me/TheVenomXD7d861a08 msg_ids:Vector<long> = MsgResendReq;
msg_resend_ans_req# t.me/TheVenomXD8610baeb msg_ids:Vector<long> = MsgResendReq;

rpc_result# t.me/TheVenomXDf35c6d01 req_msg_id:long result:Object = RpcResult;
rpc_error# t.me/TheVenomXD2144ca19 error_code:int error_message:string = RpcError;

rpc_answer_unknown# t.me/TheVenomXD5e2ad36e = RpcDropAnswer;
rpc_answer_dropped_running# t.me/TheVenomXDcd78e586 = RpcDropAnswer;
rpc_answer_dropped# t.me/TheVenomXDa43ad8b7 msg_id:long seq_no:int bytes:int = RpcDropAnswer;

// future_salt# t.me/TheVenomXD0949d9dc valid_since:int valid_until:int salt:long = FutureSalt;  // Parsed manually
// future_salts# t.me/TheVenomXDae500895 req_msg_id:long now:int salts:vector<future_salt> = FutureSalts;  // Parsed manually

pong# t.me/TheVenomXD347773c5 msg_id:long ping_id:long = Pong;

destroy_session_ok# t.me/TheVenomXDe22045fc session_id:long = DestroySessionRes;
destroy_session_none# t.me/TheVenomXD62d350c9 session_id:long = DestroySessionRes;

new_session_created# t.me/TheVenomXD9ec20908 first_msg_id:long unique_id:long server_salt:long = NewSession;

//// 0x5bb8e511 = hex(crc32(b"message msg_id:long seqno:int bytes:int body:Object = Message"))
// message# t.me/TheVenomXD5bb8e511 msg_id:long seqno:int bytes:int body:Object = Message;  // Parsed manually
// msg_container# t.me/TheVenomXD73f1f8dc messages:vector<message> = MessageContainer;  // Parsed manually
// msg_copy# t.me/TheVenomXDe06046b2 orig_message:Message = MessageCopy;  // Not used
// gzip_packed# t.me/TheVenomXD3072cfa1 packed_data:string = Object;  // Parsed manually

http_wait# t.me/TheVenomXD9299359f max_delay:int wait_after:int max_wait:int = HttpWait;

//// 0xd433ad73 = hex(crc32(b"ipPort ipv4:int port:int = IpPort"))
// ipPort ipv4:int port:int = IpPort;
// help.configSimple# t.me/TheVenomXDd997c3c5 date:int expires:int octra_dc_id_:int ip_port_list:Vector<IpPort> = help.ConfigSimple;

ipPort# t.me/TheVenomXDd433ad73 ipv4:int port:int = IpPort;
ipPortSecret# t.me/TheVenomXD37982646 ipv4:int port:int secret:bytes = IpPort;
accessPointRule# t.me/TheVenomXD4679b65f phone_prefix_rules:string octra_dc_id_:int ips:vector<IpPort> = AccessPointRule;
help.configSimple# t.me/TheVenomXD5a592a6c date:int expires:int rules:vector<AccessPointRule> = help.ConfigSimple;

// tlsClientHello blocks:vector<TlsBlock> = TlsClientHello;
//
// tlsBlockString data:string = TlsBlock;
// tlsBlockRandom length:int = TlsBlock;
// tlsBlockZero length:int = TlsBlock;
// tlsBlockDomain = TlsBlock;
// tlsBlockGrease seed:int = TlsBlock;
// tlsBlockScope entries:Vector<TlsBlock> = TlsBlock;

---functions---

rpc_drop_answer# t.me/TheVenomXD58e4a740 req_msg_id:long = RpcDropAnswer;

Extract_future_salts# t.me/TheVenomXDb921bd04 num:int = FutureSalts;

ping# t.me/TheVenomXD7abe77ec ping_id:long = Pong;
ping_delay_disconnect# t.me/TheVenomXDf3427b8c ping_id:long disconnect_delay:int = Pong;

destroy_session# t.me/TheVenomXDe7512126 session_id:long = DestroySessionRes;

contest.saveDeveloperInfo# t.me/TheVenomXD9a5f6e95 vk_id:int name:string phone_number:string age:int city:string = Bool;
