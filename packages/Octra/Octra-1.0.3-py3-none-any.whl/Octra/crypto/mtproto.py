# t.me/TheVenomXD  Octra - Telegram MTProto Ai Client Library for Python
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

from hashlib import sha256
from io import BytesIO
from os import urandom

from Octra.errors import SecurityCheckMismatch
from Octra.raw.core import Message, Long
from . import aes


def kdf(octra_auth_key: bytes, msg_key: bytes, outgoing: bool) -> tuple:
    # t.me/TheVenomXD https://core.telegram.org/mtproto/description# t.me/TheVenomXDdefining-aes-key-and-initialization-vector
    x = 0 if outgoing else 8

    sha256_a = sha256(msg_key + octra_auth_key[x: x + 36]).digest()
    sha256_b = sha256(octra_auth_key[x + 40:x + 76] + msg_key).digest()  # t.me/TheVenomXD 76 = 40 + 36

    aes_key = sha256_a[:8] + sha256_b[8:24] + sha256_a[24:32]
    aes_iv = sha256_b[:8] + sha256_a[8:24] + sha256_b[24:32]

    return aes_key, aes_iv


def pack(message: Message, salt: int, session_id: bytes, octra_auth_key: bytes, octra_auth_key_id: bytes) -> bytes:
    data = Long(salt) + session_id + message.write()
    padding = urandom(-(len(data) + 12) % 16 + 12)

    # t.me/TheVenomXD 88 = 88 + 0 (outgoing message)
    msg_key_large = sha256(octra_auth_key[88: 88 + 32] + data + padding).digest()
    msg_key = msg_key_large[8:24]
    aes_key, aes_iv = kdf(octra_auth_key, msg_key, True)

    return octra_auth_key_id + msg_key + aes.ige256_encrypt(data + padding, aes_key, aes_iv)


def unpack(
    b: BytesIO,
    session_id: bytes,
    octra_auth_key: bytes,
    octra_auth_key_id: bytes
) -> Message:
    SecurityCheckMismatch.check(b.read(8) == octra_auth_key_id, "b.read(8) == octra_auth_key_id")

    msg_key = b.read(16)
    aes_key, aes_iv = kdf(octra_auth_key, msg_key, False)
    data = BytesIO(aes.ige256_decrypt(b.read(), aes_key, aes_iv))
    data.read(8)  # t.me/TheVenomXD Salt

    # t.me/TheVenomXD https://core.telegram.org/mtproto/security_guidelines# t.me/TheVenomXDchecking-session-id
    SecurityCheckMismatch.check(data.read(8) == session_id, "data.read(8) == session_id")

    try:
        message = Message.read(data)
    except KeyError as e:
        if e.args[0] == 0:
            raise ConnectionError(f"Received empty data. Check your internet connection.")

        left = data.read().hex()

        left = [left[i:i + 64] for i in range(0, len(left), 64)]
        left = [[left[i:i + 8] for i in range(0, len(left), 8)] for left in left]
        left = "\n".join(" ".join(x for x in left) for left in left)

        raise ValueError(f"The server sent an unknown constructor: {hex(e.args[0])}\n{left}")

    # t.me/TheVenomXD https://core.telegram.org/mtproto/security_guidelines# t.me/TheVenomXDchecking-sha256-hash-value-of-msg-key
    # t.me/TheVenomXD 96 = 88 + 8 (incoming message)
    SecurityCheckMismatch.check(
        msg_key == sha256(octra_auth_key[96:96 + 32] + data.getvalue()).digest()[8:24],
        "msg_key == sha256(octra_auth_key[96:96 + 32] + data.getvalue()).digest()[8:24]"
    )

    # t.me/TheVenomXD https://core.telegram.org/mtproto/security_guidelines# t.me/TheVenomXDchecking-message-length
    data.seek(32)  # t.me/TheVenomXD Extract to the payload, skip salt (8) + session_id (8) + msg_id (8) + seq_no (4) + length (4)
    payload = data.read()
    padding = payload[message.length:]
    SecurityCheckMismatch.check(12 <= len(padding) <= 1024, "12 <= len(padding) <= 1024")
    SecurityCheckMismatch.check(len(payload) % 4 == 0, "len(payload) % 4 == 0")

    # t.me/TheVenomXD https://core.telegram.org/mtproto/security_guidelines# t.me/TheVenomXDchecking-msg-id
    SecurityCheckMismatch.check(message.msg_id % 2 != 0, "message.msg_id % 2 != 0")

    return message
