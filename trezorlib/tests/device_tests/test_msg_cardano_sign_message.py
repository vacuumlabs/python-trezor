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

from binascii import hexlify

import pytest

from trezorlib.cardano import sign_message
from trezorlib.tools import parse_path

from .common import TrezorTest


@pytest.mark.cardano
@pytest.mark.skip_t1  # T1 support is not planned
class TestMsgCardanoSignMessage(TrezorTest):
    @pytest.mark.parametrize(
        "message,path,expected_signature",
        [
            (
                "Test message to sign",
                "m/44'/1815'/0'/0/0",
                "71b788005262ad1ba99e8a9e723066780c3b02da360e7ceb7e656a4e115cc090ab4def812fdf1090f5db246c3922cd4869bfda181e377b957bc738b57d481f0e",
            ),
            (
                "New Test message to sign",
                "m/44'/1815'/0'/0/1",
                "4770ead4d4b5f3a160c77bf3794b19bf4cf154955ea0162ef37967665286ceeb292dec1225d545d979deeaab9b7437e7bc9045eb627083a0dbd389f1d59df500",
            ),
            (
                "Another Test message to sign",
                "m/44'/1815'/0'/0/2",
                "1f858f9f5fff1deed9cf7ac8d40511d09080395c90e881a164dd0a862fd5367b8ffd915a01ae45cfceac0c96272d6a3b66f5dc54af3d0666a034f8b5aadaaf08",
            ),
            (
                "Just another Test message to sign",
                "m/44'/1815'/0'/0/3",
                "2b7fde2b4665f72d40693e2f337ce7452bd5b6afe8c88417f9705d6f28ffbc9cf3b2e5e255946d307fc9654aae33667651923048b812d8070a9d53d620e36703",
            ),
        ],
    )
    def test_cardano_sign_message(self, message, path, expected_signature):
        self.setup_mnemonic_allallall()

        signature = sign_message(self.client, parse_path(path), message)
        assert expected_signature == hexlify(signature.signature).decode("utf8")
