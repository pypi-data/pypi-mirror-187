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

from typing import Tuple


class DataCenter:
    TEST = {
        1: "149.154.175.10",
        2: "149.154.167.40",
        3: "149.154.175.117",
    }

    PROD = {
        1: "149.154.175.53",
        2: "149.154.167.51",
        3: "149.154.175.100",
        4: "149.154.167.91",
        5: "91.108.56.130"
    }

    PROD_MEDIA = {
        2: "149.154.167.151",
        4: "149.154.164.250"
    }

    TEST_IPV6 = {
        1: "2001:b28:f23d:f001::e",
        2: "2001:67c:4e8:f002::e",
        3: "2001:b28:f23d:f003::e",
    }

    PROD_IPV6 = {
        1: "2001:b28:f23d:f001::a",
        2: "2001:67c:4e8:f002::a",
        3: "2001:b28:f23d:f003::a",
        4: "2001:67c:4e8:f004::a",
        5: "2001:b28:f23f:f005::a"
    }

    PROD_IPV6_MEDIA = {
        2: "2001:067c:04e8:f002:0000:0000:0000:000b",
        4: "2001:067c:04e8:f004:0000:0000:0000:000b"
    }

    def __new__(cls, octra_dc_id_: int, octra_test_mode: bool, ipv6: bool, media: bool) -> Tuple[str, int]:
        if octra_test_mode:
            if ipv6:
                ip = cls.TEST_IPV6[octra_dc_id_]
            else:
                ip = cls.TEST[octra_dc_id_]

            return ip, 80
        else:
            if ipv6:
                if media:
                    ip = cls.PROD_IPV6_MEDIA.get(octra_dc_id_, cls.PROD_IPV6[octra_dc_id_])
                else:
                    ip = cls.PROD_IPV6[octra_dc_id_]
            else:
                if media:
                    ip = cls.PROD_MEDIA.get(octra_dc_id_, cls.PROD[octra_dc_id_])
                else:
                    ip = cls.PROD[octra_dc_id_]

            return ip, 443
