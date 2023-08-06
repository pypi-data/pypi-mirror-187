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

from .exceptions import *
from .rpc_error import UnknownError


class BadMsgNotification(Exception):
    descriptions = {
        16: "The msg_id is too low, the client time has to be synchronized.",
        17: "The msg_id is too high, the client time has to be synchronized.",
        18: "Incorrect two lower order of the msg_id bits, the server expects the client message "
            "msg_id to be divisible by 4.",
        19: "The container msg_id is the same as the msg_id of a previously received message.",
        20: "The message is too old, it cannot be verified by the server.",
        32: "The msg_seqno is too low.",
        33: "The msg_seqno is too high.",
        34: "An even msg_seqno was expected, but an odd one was received.",
        35: "An odd msg_seqno was expected, but an even one was received.",
        48: "Incorrect server salt.",
        64: "Invalid container."
    }

    def __init__(self, code):
        description = self.descriptions.get(code, "Unknown error code")
        super().__init__(f"[{code}] {description}")


class SecurityError(Exception):
    """Generic security error."""

    @classmethod
    def check(cls, cond: bool, msg: str):
        """Raises this exception if the condition is false"""
        if not cond:
            raise cls(f"Check failed: {msg}")


class SecurityCheckMismatch(SecurityError):
    """Raised when a security check mismatch occurs."""

    def __init__(self, msg: str = None):
        super().__init__("A security check mismatch has occurred." if msg is None else msg)


class CDNFileHashMismatch(SecurityError):
    """Raised when a CDN file hash mismatch occurs."""

    def __init__(self, msg: str = None):
        super().__init__("A CDN file hash mismatch has occurred." if msg is None else msg)
