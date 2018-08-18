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
from trezorlib.cardano import get_address
from trezorlib.tools import parse_path


@pytest.mark.cardano
@pytest.mark.skip_t1  # T1 support is not planned
class TestMsgCardanoGetAddress(TrezorTest):

    def test_cardano_get_address_v1(self):
        # data from https://iancoleman.io/bip39/#english
        self.setup_mnemonic_nopin_nopassphrase()

        address = get_address(self.client, parse_path("m/44'/1815'/0'/0/0")).address
        assert address == '2w1sdSJu3GVfqnGAyqAdaWrN8Txv1vCZTN1Pe2AA54ysjWNbNzma3WVtSJfMc6HpM9KEQsdJ7oALPwfQWesRp8QDsFRQpzuNrdq'
        address = get_address(self.client, parse_path("m/44'/1815'/0'/0/1")).address
        assert address == '2w1sdSJu3GVhMmEYeGYEPWahV1V17pFw59GfgqjSRqa6x1rKFxbyCZrQWLe78xdSx3zyed6DrrN5yMgoY7ST2vJeaMzUDB7W3WG'
        address = get_address(self.client, parse_path("m/44'/1815'/0'/0/2")).address
        assert address == '2w1sdSJu3GVeHCDfy3mjq8RkzkN3Vh7Di3cB8NRzkwkLQ2FAjxX1kvkNdP9hNBzyBVEJdeWwyb5GfFYXgKe7rPgvWj2QD8FE4W3'
