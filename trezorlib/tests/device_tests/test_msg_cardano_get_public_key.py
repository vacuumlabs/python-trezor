# This file is part of the Trezor project.
#
# Copyright (C) 2012-2018 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import pytest

from .common import TrezorTest
from binascii import hexlify
from trezorlib.cardano import get_public_key
from trezorlib.tools import parse_path


@pytest.mark.cardano
@pytest.mark.skip_t1  # T1 support is not planned
class TestMsgCardanoGetPublicKey(TrezorTest):

    def test_cardano_v1_get_public_key(self):
        # https://github.com/trezor/trezor-core/blob/master/tests/test_apps.cardano.get_public_key.py
        self.client.load_device_by_mnemonic(
            mnemonic='plastic that delay conduct police ticket swim gospel intact harsh obtain entire',
            pin='',
            passphrase_protection=False,
            label='test',
            language='english')

        derivation_paths = [
            "m/44'/1815'/0'",
            "m/44'/1815'/1'",
            "m/44'/1815'/2'",
            "m/44'/1815'/3'",
        ]

        root_hd_passphrase = '8ee689a22e1ec569d2ada515c4ee712ad089901b7fe0afb94fe196de944ee814'

        public_keys = [
            'dcb047bcede0f61f2f1966f79bfaf20afe8c987c259cfa9e8e17be4fdc6eb6c4',
            '3b1bf9b06b77f485c35cf541427872e07b2a7091e9d3685e8664dea728f4cab4',
            'cb338f45b7fdda44c29a407e256360ece5e915f41b7f9eda564d1168d2e0bff0',
            '647912d68833b361be03f8e715c4234638161de715f2072208dc94675c4742e7',
        ]

        chain_codes = [
            'cadec3c434d90493717a12bc505c793d52473db8005eae6cf7e9275d746d339b',
            'a8f5dcbbcdb56f007847bbacb6df5837e84e3ce9c1a927b31e8baa31560cd195',
            'a7e41f0163e7b12632cef40fdeff73db75230a0a25122fcc83dc56a8109e611a',
            '4b9217f481318cbc15eea77c48d9bca707d8c953538b8d6081503a3481c67f3b',
        ]

        xpub_keys = [
            'dcb047bcede0f61f2f1966f79bfaf20afe8c987c259cfa9e8e17be4fdc6eb6c4cadec3c434d90493717a12bc505c793d52473db8005eae6cf7e9275d746d339b',
            '3b1bf9b06b77f485c35cf541427872e07b2a7091e9d3685e8664dea728f4cab4a8f5dcbbcdb56f007847bbacb6df5837e84e3ce9c1a927b31e8baa31560cd195',
            'cb338f45b7fdda44c29a407e256360ece5e915f41b7f9eda564d1168d2e0bff0a7e41f0163e7b12632cef40fdeff73db75230a0a25122fcc83dc56a8109e611a',
            '647912d68833b361be03f8e715c4234638161de715f2072208dc94675c4742e74b9217f481318cbc15eea77c48d9bca707d8c953538b8d6081503a3481c67f3b',
        ]

        for index, derivation_path in enumerate(derivation_paths):
            key = get_public_key(self.client, parse_path(derivation_path))

            assert hexlify(key.node.public_key).decode('utf8') == public_keys[index]
            assert hexlify(key.node.chain_code).decode('utf8') == chain_codes[index]
            assert key.xpub == xpub_keys[index]
            assert key.root_hd_passphrase == root_hd_passphrase
