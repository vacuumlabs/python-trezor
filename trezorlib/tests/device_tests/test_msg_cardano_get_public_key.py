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

from trezorlib.cardano import get_public_key
from trezorlib.tools import parse_path

from .common import TrezorTest


@pytest.mark.cardano
@pytest.mark.skip_t1  # T1 support is not planned
class TestMsgCardanoGetPublicKey(TrezorTest):
    @pytest.mark.parametrize(
        "path,public_key,chain_code",
        [
            (
                "m/44'/1815'/0'",
                "619ca242c1c4037c562d42208e118a94aeb7b895a82e4d0a3656b93b432b2a18",
                "7ad6955a9a351d3a018782d579d3c42d87f173fe59bbb149ce235cb8b294b58c",
            ),
            (
                "m/44'/1815'/1'",
                "be9c6cde709851b498edac5de832ffa57f9350f46c15befce53c656aa3d1e5c8",
                "93ec0b00fd667745311b54fdc4d7ebc8c85935bb968632bd89a4bb74520b11b8",
            ),
            (
                "m/44'/1815'/2'",
                "036bd9920233613e414df360fc296e6bfac630207a1ec1e1f5a0fc15263b132b",
                "6beeed4c774e5683bd67645307f5e81a6d17a2e6c39e5852f1d581dfd67f37e5",
            ),
            (
                "m/44'/1815'/3'",
                "5b60d6c9b1809ca551dd469253e9ce99f072731aa996849eaf558310e62e0ed1",
                "6d9bbe6c48f006429266268f4e2cc9c350a2f42bcb8b86c2c4d7053e17394025",
            ),
        ],
    )
    def test_cardano_v1_get_public_key(self, path, public_key, chain_code):
        self.setup_mnemonic_allallall()

        root_hd_passphrase = (
            "977dfbe0e80f01e2d8b160100dd6327ec8bddbcb36efc5fb0c32a710b0e69fcb"
        )

        key = get_public_key(self.client, parse_path(path))

        assert hexlify(key.node.public_key).decode("utf8") == public_key
        assert hexlify(key.node.chain_code).decode("utf8") == chain_code
        assert key.xpub == public_key + chain_code
        assert key.root_hd_passphrase == root_hd_passphrase
