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
from trezorlib.cardano import sign_message
from trezorlib.tools import parse_path


@pytest.mark.cardano
@pytest.mark.skip_t1  # T1 support is not planned
class TestMsgCardanoGetPublicKey(TrezorTest):

    def test_cardano_get_public_key(self):
        self.client.load_device_by_mnemonic(
            mnemonic='plastic that delay conduct police ticket swim gospel intact harsh obtain entire',
            pin='',
            passphrase_protection=False,
            label='test',
            language='english')

        correct_messages = [
            ('Test message to sign', "m/44'/1815'/0'/0/0", 'c86eac56d3d3b8b3658363107479e7ec4e7155f5cb0a1459f68f6da7192f4f58c2b487b0617c575d941e1a9edcc8e41f6512b581e47282542ed5aab00613fc04'),
            ('New Test message to sign', "m/44'/1815'/0'/0/1", '10fa0ba6705a34e8a6f4af77fb20939a5102e7391fcd26e038ae387e91152b49c26d4d6a1f270a84bd04473f4689e06368997ba740dc2b35fddfe7a07de1a307'),
            ('Another Test message to sign', "m/44'/1815'/0'/0/2", '72d0b49f072b9c4cf3d034e2ef602b4fe5a601423f3340aa91c23809675442354bfe9a8bf0f127416e79229931b4261709e1f2d513cf596835ce83939aa24108'),
            ('Just another Test message to sign', "m/44'/1815'/0'/0/3", '796b66b54f79816bffa5ae48eb7bbbddce96c4a40a85e5aa9fb17fe30b0da8b689a62d47897b6471b6d595a5180c9cbd9c8c6c78486e214e0d759b17681ff404'),
        ]

        for (message, derivation_path, expected_signature) in correct_messages:
            signature = sign_message(self.client, parse_path(derivation_path), message)
            assert expected_signature == hexlify(signature.signature).decode('utf8')

        incorrect_messages = [
            ('Test message to sign fail', "m/44'/1815'/0'/0/0", 'c86eac56d3d3b8b3658363107479e7ec4e7155f5cb0a1459f68f6da7192f4f58c2b487b0617c575d941e1a9edcc8e41f6512b581e47282542ed5aab00613fc04'),
            ('New Test message to sign', "m/44'/1815'/0'/0/1", '20fa0ba6705a34e8a6f4af77fb20939a5102e7391fcd26e038ae387e91152b49c26d4d6a1f270a84bd04473f4689e06368997ba740dc2b35fddfe7a07de1a307'),
            ('Another Test message to sign fail', "m/44'/1815'/0'/0/2", '20d0b49f072b9c4cf3d034e2ef602b4fe5a601423f3340aa91c23809675442354bfe9a8bf0f127416e79229931b4261709e1f2d513cf596835ce83939aa24108'),
            ('Just another Test message to sign', "m/44'/1815'/0'/0/4", '796b66b54f79816bffa5ae48eb7bbbddce96c4a40a85e5aa9fb17fe30b0da8b689a62d47897b6471b6d595a5180c9cbd9c8c6c78486e214e0d759b17681ff404'),
        ]

        for (message, derivation_path, expected_signature) in incorrect_messages:
            signature = sign_message(self.client, parse_path(derivation_path), message)
            assert expected_signature != hexlify(signature.signature).decode('utf8')
